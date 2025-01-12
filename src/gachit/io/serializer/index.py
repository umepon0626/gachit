import math
from hashlib import sha1
from pathlib import Path

from gachit.domain.entity import Index, IndexEntry, Sha


class IndexSerializer:
    @staticmethod
    def deserialize(data: bytes) -> Index:
        # read the header
        header = data[:12]
        signature = header[:4]
        assert signature == b"DIRC", "Invalid index file signature"
        version = int.from_bytes(header[4:8], "big")
        assert version in (2,), f"Unsupported index version {version}"
        count = int.from_bytes(header[8:12], "big")

        # read the entries
        entries: list[IndexEntry] = []
        content = data[12:]
        idx = 0
        for _ in range(count):
            ctime_s = int.from_bytes(content[idx : idx + 4])
            ctime_ns = int.from_bytes(content[idx + 4 : idx + 8])

            mtime_s = int.from_bytes(content[idx + 8 : idx + 12])
            mtime_ns = int.from_bytes(content[idx + 12 : idx + 16])

            dev = int.from_bytes(content[idx + 16 : idx + 20], "big")
            inode = int.from_bytes(content[idx + 20 : idx + 24], "big")
            # Ignored.
            unused = int.from_bytes(content[idx + 24 : idx + 26], "big")
            assert unused == 0
            mode = int.from_bytes(content[idx + 26 : idx + 28], "big")
            mode_type = mode >> 12
            assert mode_type in [0b1000, 0b1010, 0b1110]
            mode_perms = mode & 0b0000000111111111
            # User ID
            uid = int.from_bytes(content[idx + 28 : idx + 32], "big")
            # Group ID
            gid = int.from_bytes(content[idx + 32 : idx + 36], "big")
            # Size
            fsize = int.from_bytes(content[idx + 36 : idx + 40], "big")
            sha = Sha(
                format(int.from_bytes(content[idx + 40 : idx + 60], "big"), "040x")
            )
            # Flags we're going to ignore
            flags = int.from_bytes(content[idx + 60 : idx + 62], "big")
            # Parse flags
            flag_assume_valid = (flags & 0b1000000000000000) != 0
            flag_extended = (flags & 0b0100000000000000) != 0
            assert not flag_extended
            flag_stage = flags & 0b0011000000000000
            # Length of the name.  This is stored on 12 bits, some max
            # value is 0xFFF, 4095.  Since names can occasionally go
            # beyond that length, git treats 0xFFF as meaning at least
            # 0xFFF, and looks for the final 0x00 to find the end of the
            # name --- at a small, and probably very rare, performance
            # cost.
            name_length = flags & 0b0000111111111111

            # We've read 62 bytes so far.
            idx += 62

            if name_length < 0xFFF:
                assert content[idx + name_length] == 0x00
                raw_name = content[idx : idx + name_length]
                idx += name_length + 1
            else:
                null_idx = content.find(b"\x00", idx + 0xFFF)
                raw_name = content[idx:null_idx]
                idx = null_idx + 1

            # Just parse the name as utf8.
            name = raw_name.decode("utf8")
            idx = 8 * math.ceil(idx / 8)

            entries.append(
                IndexEntry(
                    ctime=(ctime_s, ctime_ns),
                    mtime=(mtime_s, mtime_ns),
                    dev=dev,
                    inode=inode,
                    mode_type=mode_type,
                    mode_perms=mode_perms,
                    uid=uid,
                    gid=gid,
                    fsize=fsize,
                    sha=sha,
                    flag_assume_valid=bool(flag_assume_valid),
                    flag_stage=bool(flag_stage),
                    path=Path(name),
                )
            )
        return Index(version=version, entries=entries)

    @staticmethod
    def serialize(index: Index) -> bytes:
        dst = b""
        dst += b"DIRC"
        dst += index.version.to_bytes(4, "big")
        dst += len(index.entries).to_bytes(4, "big")

        idx = 0

        for e in index.entries:
            dst += e.ctime[0].to_bytes(4, "big")
            dst += e.ctime[1].to_bytes(4, "big")
            dst += e.mtime[0].to_bytes(4, "big")
            dst += e.mtime[1].to_bytes(4, "big")
            dst += e.dev.to_bytes(4, "big")
            dst += e.inode.to_bytes(4, "big")

            mode = (e.mode_type << 12) | e.mode_perms
            dst += mode.to_bytes(4, "big")

            dst += e.uid.to_bytes(4, "big")
            dst += e.gid.to_bytes(4, "big")

            dst += e.fsize.to_bytes(4, "big")
            dst += int(e.sha.value, 16).to_bytes(20, "big")

            flag_assume_valid = 0x1 << 15 if e.flag_assume_valid else 0

            name_bytes = str(e.path).encode("utf8")
            bytes_len = len(name_bytes)
            if bytes_len >= 0xFFF:
                name_length = 0xFFF
            else:
                name_length = bytes_len

            # We merge back three pieces of data (two flags and the
            # length of the name) on the same two byinode.
            dst += (flag_assume_valid | e.flag_stage | name_length).to_bytes(2, "big")

            # Write back the name, and a final 0x00.
            dst += name_bytes
            dst += (0).to_bytes(1, "big")

            idx += 62 + len(name_bytes) + 1

            # Add padding if necessary.
            if idx % 8 != 0:
                pad = 8 - (idx % 8)
                dst += (0).to_bytes(pad, "big")
                idx += pad

        sha1_hash = sha1(dst).digest()
        dst += sha1_hash
        return dst

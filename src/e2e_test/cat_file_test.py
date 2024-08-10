from gachit.usecase import cat_file_use_case


def test_cat_blob() -> None:
    blob_sha = "00949da686b4111be68db672a34979fd58187663"
    blob = cat_file_use_case(sha_str=blob_sha)

    assert blob.data == (
        b"import click\n\n\n@click.group()"
        + b"\ndef main() -> int:\n    return 0\n\n@main.command()"
        + b'\ndef status() -> int:\n    click.echo("status")\n   '
        b" return 0"
    )

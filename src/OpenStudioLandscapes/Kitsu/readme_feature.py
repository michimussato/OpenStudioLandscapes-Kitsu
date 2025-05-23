import textwrap
import snakemd


def readme_feature(doc: snakemd.Document) -> snakemd.Document:

    ## Some Specific information

    doc.add_heading(
        text="Kitsu Documentation",
        level=2,
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo Kitsu
                """
            ),
            image={
                "Kitsu": "https://camo.githubusercontent.com/023fe0d7cf9dc4bd4258a299a718a8c98d94be4357d72dfda0fcb0217ba1582c/68747470733a2f2f7a6f752e63672d776972652e636f6d2f6b697473752e706e67",
            }["Kitsu"],
            link="https://github.com/cgwire/zou",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Kitsu is written and maintained by CGWire, a company based
            in France:
            """
        )
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent(
                """
                Logo CGWire
                """
            ),
            image={
                "CGWire": "https://www.cg-wire.com/_nuxt/logo.4d5a2d7e.png",
            }["CGWire"],
            link="https://www.cg-wire.com/",
        ).__str__()
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Kitsu itself consists of two modules:
            """
        )
    )

    doc.add_ordered_list(
        [
            "[Gazu - Kitsu Python Client](https://gazu.cg-wire.com/)",
            "[Zou - Kitsu Python API](https://zou.cg-wire.com/)",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            `OpenStudioLandscapes-Kitsu` is based on the Kitsu provided
            Docker image:
            """
        )
    )

    doc.add_ordered_list(
        [
            "[https://kitsu.cg-wire.com/installation/#using-docker-image]()",
            "[https://hub.docker.com/r/cgwire/cgwire]()",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            The default credentials are:
            """
        )
    )

    doc.add_ordered_list(
        [
            "User: `admin@example.com`",
            "Password: `mysecretpassword`",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            You can override the default credentials by setting:
            """
        )
    )

    doc.add_ordered_list(
        [
            "`KITSU_ADMIN_USER`",
            "`KITSU_DB_PASSWORD`",
        ]
    )

    return doc


if __name__ == "__main__":
    pass

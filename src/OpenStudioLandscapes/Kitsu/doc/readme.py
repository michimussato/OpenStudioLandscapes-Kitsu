import textwrap

import snakemd


def readme_feature(
    doc: snakemd.Document,
    main_header: str,
) -> snakemd.Document:

    # Some Specific information

    doc.add_heading(
        text=main_header,
        level=1,
    )

    doc.add_unordered_list(
        [
            "[https://kitsu.cg-wire.com](https://kitsu.cg-wire.com)",
        ]
    )

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent("""\
                Logo Kitsu\
                """),
            image={
                "Kitsu": "https://zou.cg-wire.com/kitsu.png",
            }["Kitsu"],
            link="https://github.com/cgwire/zou",
        ).__str__()
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            Kitsu is written and maintained by CGWire, a company based
            in France:\
            """))

    # Logo

    doc.add_paragraph(
        snakemd.Inline(
            text=textwrap.dedent("""\
                Logo CGWire\
                """),
            image={
                "CGWire": "https://www.cg-wire.com/_nuxt/logo.4d5a2d7e.png",
            }["CGWire"],
            link="https://www.cg-wire.com",
        ).__str__()
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            Kitsu itself consists of two modules:\
            """))

    doc.add_ordered_list(
        [
            "[Gazu - Kitsu Python Client](https://gazu.cg-wire.com)",
            "[Zou - Kitsu Python API](https://zou.cg-wire.com)",
        ]
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            `OpenStudioLandscapes-Kitsu` is based on the Kitsu provided
            Docker image:\
            """))

    doc.add_unordered_list(
        [
            "[https://kitsu.cg-wire.com/installation/#using-docker-image](https://kitsu.cg-wire.com/installation/#using-docker-image)",
            "[https://hub.docker.com/r/cgwire/cgwire](https://hub.docker.com/r/cgwire/cgwire)",
        ]
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            The default credentials are:\
            """))

    doc.add_unordered_list(
        [
            "User: `admin@example.com`",
            "Password: `mysecretpassword`",
        ]
    )

    doc.add_heading(
        text="Inofficial Resources",
        level=2,
    )

    doc.add_paragraph(text=textwrap.dedent("""\
            An interesting Docker Compose project for Kitsu
            worth following can be found below. 
            OpenStudioLandscapes-Kitsu, however, is not based on 
            this project but may one day leverage it:\
            """))

    doc.add_ordered_list(
        [
            "[Mathieu BOUZARD/docker-cgwire](https://gitlab.com/mathbou/docker-cgwire)",
        ]
    )

    doc.add_horizontal_rule()

    return doc


if __name__ == "__main__":
    pass

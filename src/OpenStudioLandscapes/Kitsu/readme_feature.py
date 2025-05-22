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

    doc.add_heading(
        text="Get Deadline 10.2",
        level=3,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Deadline is free, however (legally), an AWS account is required to access the download area.
            Also, the account is required to use all Deadline features. Register here:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[https://portal.aws.amazon.com/billing/signup]()",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Once logged in, you can download the Deadline tar archive from this website:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[https://us-east-1.console.aws.amazon.com/deadlinecloud/home#/thinkbox]()",
        ]
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            If you prefer to just download Deadline and use it without any AWS Cloud features,
            here you can get the `tar` archive and the `sha256` directly:
            """
        )
    )

    doc.add_unordered_list(
        [
            "[https://thinkbox-installers.s3.us-west-2.amazonaws.com/Releases/Deadline/10.2/5_10.2.1.1/Deadline-10.2.1.1-linux-installers.tar]()",
            "[https://thinkbox-installers.s3.us-west-2.amazonaws.com/Releases/Deadline/10.2/5_10.2.1.1/Deadline-10.2.1.1-linux-installers.sha256]()",
        ]
    )

    doc.add_heading(
        text="Instructions",
        level=3,
    )

    doc.add_paragraph(
        text=textwrap.dedent(
            """
            Extract all contents for the `tar` archive to `OpenStudioLandscapes-Deadline-10-2/.payload/bin`.
            """
        )
    )

    doc.add_heading(
        text="Documentation",
        level=2,
    )

    doc.add_heading(
        text="User Manual",
        level=3,
    )

    doc.add_unordered_list(
        [
            "[https://docs.thinkboxsoftware.com/products/deadline/10.2/1_User%20Manual/index.html]()",
        ]
    )

    doc.add_heading(
        text="Scripting Reference",
        level=3,
    )

    doc.add_unordered_list(
        [
            "[https://docs.thinkboxsoftware.com/products/deadline/10.2/2_Scripting%20Reference/index.html]()",
        ]
    )

    doc.add_heading(
        text="Python Reference",
        level=3,
    )

    doc.add_unordered_list(
        [
            "[https://docs.thinkboxsoftware.com/products/deadline/10.2/3_Python%20Reference/index.html]()",
        ]
    )

    doc.add_heading(
        text="Information on Usage Based Licensing (UBL)",
        level=3,
    )

    doc.add_unordered_list(
        [
            "[https://marketplace.thinkboxsoftware.com]()",
            "[https://awsthinkbox.zendesk.com/hc/en-us/articles/22883209044759-AWS-Deadline-Cloud-UBL-for-Deadline-10-on-AWS]()",
        ]
    )

    return doc


if __name__ == "__main__":
    pass

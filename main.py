import click


@click.command()
@click.option(
    "--config", envvar="CONFIG", default="/etc/kubespary/sync.yaml", help="Configuration for sync", type=click.Path()
)
def main(config):
    pass


if __name__ == "__main__":
	# pylint: disable=no-value-for-parameter
	# pylint: disable=unexpected-keyword-arg
    main(auto_envvar_prefix="SYNC_")

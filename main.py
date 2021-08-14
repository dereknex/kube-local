import click
from config import Configuration
from task import Manager


@click.command()
@click.option(
    "--config", envvar="CONFIG", default="/etc/kubespary/sync.yaml", help="Configuration for sync", type=click.Path()
)
def main(config):
    m = Manager(Configuration(config))
    m.run()


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    # pylint: disable=unexpected-keyword-arg
    main(auto_envvar_prefix="SYNC_")

from datetime import datetime, timedelta
from typing import Optional

import click
from click import BadParameter

from pepy.application.command import UpdateVersionDownloads
from pepy.domain.model import Password
from pepy.infrastructure import container


@click.group()
def cli():
    pass


@cli.command("import:downloads:day")
@click.option("--day", help="The day to import downloads")
@click.option("--password", prompt=True, help="The day to import downloads")
def import_day_downloads_action(password: str, day: Optional[str]):
    try:
        if day is not None:
            date = datetime.strptime(day, "%Y-%m-%d")
        else:
            date = datetime.now() - timedelta(days=1)
    except ValueError:
        raise BadParameter("Date format should be YYYY-mm-dd")
    click.echo("Importing downloads...")
    container.command_bus.publish(UpdateVersionDownloads(date.date(), Password(password)))
    click.echo("Done")

import json
import requests
import click


@click.group()
def cli():
    pass


@cli.command()
def PostText():
    text = click.prompt("Enter your text")
    responsePost = requests.post(
        "http://host.docker.internal:8080/analysis/text",
        json={'text': text}
    )
    responsePost_dict = responsePost.json()
    responsePost = json.dumps(responsePost_dict, indent=4, ensure_ascii=False)
    click.echo(responsePost)


@cli.command()
def GetTask():
    responseGet = requests.get(
        "http://host.docker.internal:8080/analysis/jira"
    )
    responseGet_dict = responseGet.json()
    responseGet = json.dumps(responseGet_dict, indent=4, ensure_ascii=False)
    click.echo(responseGet)


if __name__ == '__main__':
    cli()
pass
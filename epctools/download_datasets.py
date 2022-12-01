import requests
from epctools.config import LA_CODES
import os
from dotenv import load_dotenv
import base64
import click
from pathlib import Path

# load environment variables - in particular we need an
# API key for the EPC data website
load_dotenv()

# this is the name of the 
EPC_FILENAME = "certificates.csv"

b64_epc_api_key = base64.b64encode(
    os.environ.get("EPC_API_KEY").encode("ascii")
).decode("ascii")


def download_epc_data(la_name: str, output_dir: str, domestic: bool=True) -> None:

    # get the code for this LA - used to construct the API
    # endpoint
    la_code = LA_CODES[la_name]

    api_dom = "https://epc.opendatacommunities.org/api/v1/domestic/"
    api_non_dom = "https://epc.opendatacommunities.org/api/v1/non-domestic/"

    if domestic:
        all_borough_dir = os.path.join(output_dir, "epc/domestic")
        data_dir = os.path.join(
            all_borough_dir,
            f"domestic-{la_code}-{la_name}",
        )
        api_endpoint = f"{api_dom}search?local-authority={la_code}"
    else:
        all_borough_dir = os.path.join(output_dir, "epc/non-domestic")
        data_dir = os.path.join(
            output_dir,  
            f"non-domestic-{la_code}-{la_name}", 
        )
        api_endpoint = f"{api_non_dom}search?local-authority={la_code}"

    # make the output directory (and parent directories)
    # if not present
    if not os.path.isdir(data_dir):
        data_path = Path(data_dir)
        data_path.mkdir(parents=True)

    # open output file and stream contents from the API
    with open(
        os.path.join(
            data_dir,
            EPC_FILENAME, 
        ),
        "wb+",
    ) as f, requests.get(
        api_endpoint,
        headers={"Accept": "text/csv", "Authorization": f"Basic {b64_epc_api_key}"},
        stream=True,
    ) as r:
        for line in r.iter_lines():
            f.write(line + b"\n")


@click.command()
@click.option(
    "--domestic",
    "dataset",
    flag_value="domestic",
    default=True
)
@click.option(
    "--non-domestic",
    "dataset",
    flag_value="non-domestic",
)
@click.option(
    "-o",
    "--output",
    default="./data",
    help="Output directory"
)
def cli(dataset, output):  
    
    is_domestic = dataset == "domestic"
    la_names = LA_CODES.keys()

    # loop over all London Boroughs and download EPC data
    for la_name in la_names:
        download_epc_data(la_name, output, domestic=is_domestic)

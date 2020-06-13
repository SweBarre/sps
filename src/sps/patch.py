import sys
from datetime import datetime
from sps import request, cache, request
from sps.helpers import print_err, line_format


def get(args):
    """Get patch information from SUSE Customer Center
    for a perticular product

    Parameters
    ----------
    args: argparse.Namespace
        product: str
            limit search to product
        arch: str
            limit search to architecture
        version: str
            limit search to version
        pattern: str
            CVE, product name, keywords to search for
        severity: str
            any, low, moderate, important, critical
        only_security_patches: bool
            if true, only security patches will be searched
        date_from: str
            search for patches starting from date %Y-%m-%d
        date_to: str
            search for patches ending at date %Y-%m-%d
        page: int
            page number to display

    Returns
    -------
    list
        a list of patches that matches the search result
        each patch is a dict

    Raises
    ------
    SystemExit
        if unable to parse args.product
        if unable to parse args.to_date or args.from_date
        if the response from SUSE Customer Center is not parsable
    """
    product = args.product if args.product else ""
    version = args.product_version if args.product_version else ""
    arch = args.arch if args.arch else ""
    product = product.replace("_", "+")
    version = version.replace("_", "+")
    if args.pattern:
        query = args.pattern.replace(" ", "+")
    else:
        query = ""
    security = "true" if args.only_security_patches else ""
    severity = "" if args.severity == "all" else args.severity

    url = "https://scc.suse.com/api/frontend/patch_finder/search/perform.json"
    url += f"?only_security_patches={security}"
    url += f"&page={args.page}"
    url += f"&product_architectures={arch}"
    url += f"&product_names={product}"
    url += f"&product_versions={version}"
    url += f"&q={query}"
    url += f"&severity={severity}"
    if args.date_to:
        try:
            datetime.strptime(args.date_to, "%Y-%m-%d")
        except ValueError:
            print_err("unable to parse --date-to")
            sys.exit(1)
        url += f"&end_issued_at={args.date_to}"
    if args.date_from:
        try:
            datetime.strptime(args.date_from, "%Y-%m-%d")
        except ValueError:
            print_err("unable to parse --date-from")
            sys.exit(1)
        url += f"&start_issued_at={args.date_from}"

    response = request.fetch(url)
    try:
        response["meta"]
        response["hits"]
    except KeyError as err:
        print(f"Could not parse response from SCC, {err}")
        sys.exit(1)
    return response


def format_detail(patch):
    """Prints a formated detailed output of every patch

    Parameters
    ----------
    patch: Dict
        a dictionary containing patch infromation from SCC

   Returns
   str
    """

    bugzilla = "\n"
    bugzilla += line_format(
        [s for s in patch["reference_entry_identifiers"] if not "CVE-" in s], indent=14
    )
    cve = "\n"
    cve += line_format(
        [s for s in patch["reference_entry_identifiers"] if "CVE-" in s], indent=14
    )
    products = " \n".join(patch["product_friendly_names"])
    packages = "\n"
    packages += line_format(patch["package_filenames"], indent=10)

    returnstr = "Detailed patch information\n"
    returnstr += "-" * 75
    returnstr += f"\nName:\t\t{patch['title']}\n"
    returnstr += f"Id:\t\t{patch['ibs_id']}\n"
    returnstr += f"Severity:\t{patch['severity']}\n"
    returnstr += f"Released:\t{patch['issued_at'][:patch['issued_at'].find('T')]}\n"
    returnstr += f"Details:\n{patch['description']}\n"
    returnstr += "References\n"
    returnstr += f"    bugzilla: {bugzilla}\n"
    returnstr += f"    cve     : {cve}\n"
    returnstr += f"Products: {products}\n"
    returnstr += f"Architecture: {' '.join(patch['product_architectures'])}\n"
    returnstr += f"Packages: {packages}"

    return returnstr

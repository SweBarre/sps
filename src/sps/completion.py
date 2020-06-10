import sys
import os
from sps.helpers import print_err
from sps import cache, patchproducts


def get(cachefile, shell=None):
    """Generates a shell completion script

    Parameters
    ----------
    cachefile: str
        Path to cache file
    shell: str, optional
        Name of the shell to generate completion script for
        if not provided the function will try to use the 
        SHELL environment varable

    Raises
    ------
    SystemExit
        if an unknown shell is provided
        if shell is not provided and SHELL environ is not set
        if completion generation file is not readable
    """

    if shell == None:
        try:
            os.environ["SHELL"]
        except KeyError:
            print_err(
                "Couldn't determin shell, you need to specify shell or set $SHELL environment variable",
            )
            sys.exit(1)
        shell = os.path.basename(os.environ.get("SHELL"))
    if shell == "bash":
        filename = f"{os.path.dirname(os.path.realpath(__file__))}/completion.sh"
    else:
        print_err(f"Unsupported shell specified '{shell}'")
        sys.exit(1)

    try:
        with open(filename, "r") as f:  # pragma: no cover
            fc = f.read()
    except FileNotFoundError as err:
        print_err({err})
        sys.exit(2)

    data = cache.load(cachefile)
    sps_patch_product_complete = " ".join(
        patchproducts.short(data["patchproducts"], "name")
    )
    sps_patch_version_complete = " ".join(
        patchproducts.short(data["patchproducts"], "version")
    )
    sps_patch_arch_complete = " ".join(
        patchproducts.short(data["patchproducts"], "architecture")
    )
    products = []
    for product in data["product"]:
        products.append(product["identifier"])
    sps_package_product_complete = " ".join(products)

    fc = fc.replace("{sps_patch_product_complete}", sps_patch_product_complete)
    fc = fc.replace("{sps_patch_version_complete}", sps_patch_version_complete)
    fc = fc.replace("{sps_patch_arch_complete}", sps_patch_arch_complete)
    fc = fc.replace("{sps_package_product_complete}", sps_package_product_complete)
    return fc

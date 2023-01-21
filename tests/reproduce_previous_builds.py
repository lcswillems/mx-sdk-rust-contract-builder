import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

downloads_folder = Path("./testdata/downloads").resolve()
extracted_folder = Path("./testdata/input/extracted").resolve()
parent_output_folder = Path("./testdata/output").resolve()
cargo_target_dir = Path("./testdata/output/cargo_target_dir").resolve()


class PreviousBuild:
    def __init__(self, name: str,
                 project_zip_url: Optional[str],
                 project_path_adjustment: Optional[str],
                 packaged_src_url: Optional[str],
                 contract_name: Optional[str],
                 expected_code_hashes: Dict[str, str],
                 docker_image: str) -> None:
        self.name = name
        self.project_zip_url = project_zip_url
        self.project_path_adjustment = project_path_adjustment
        self.packaged_src_url = packaged_src_url
        self.contract_name = contract_name
        self.expected_code_hashs = expected_code_hashes
        self.docker_image = docker_image


builds: List[PreviousBuild] = [
    PreviousBuild(
        name="a.1",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.0.0"
    ),
    PreviousBuild(
        name="a.2",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    ),
    PreviousBuild(
        name="a.3",
        project_zip_url="https://github.com/multiversx/mx-reproducible-contract-build-example-sc/archive/refs/tags/v0.1.5.zip",
        project_path_adjustment=None,
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "adder": "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
        },
        docker_image="sdk-rust-contract-builder:next"
    ),
    PreviousBuild(
        name="b.1",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.1.0"
    ),
    PreviousBuild(
        name="b.2",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.2.0"
    ),
    PreviousBuild(
        name="b.3",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/tags/v1.5.4-metabonding-unbond.zip",
        project_path_adjustment="mx-exchange-sc-1.5.4-metabonding-unbond",
        packaged_src_url=None,
        contract_name="metabonding-staking",
        expected_code_hashes={
            "metabonding-staking": "4a9b2afa13eca738b1804c48b82a961afd67adcbbf2aa518052fa124ac060bea"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.2.3"
    ),
    PreviousBuild(
        name="e.1",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.1.1-staking-upgrade.zip",
        project_path_adjustment="mx-exchange-sc-reproducible-v2.1.1-staking-upgrade",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "17a30ad44291af84f6dbd84fdaf0a9a56ed7145d544c54fd74088bb544c4f98f",
            "energy-factory": "241600c055df605cafd85b75d40b21316a6b35713485201b156d695b23c66a2f",
            "energy-factory-mock": "83b2f26a52e3fe74953f2a8cfd81f169664a4e59dae4e5d5bb1d89956fd81d43",
            "energy-update": "8523bf84ac56626c70c31342487445bf8123e3ef5f906dcb39e8b5f16c4145b7",
            "factory": "df06465b651594605466e817bfe9d8d7c68eef0f87df4a8d3266bcfb1bef6d83",
            "farm": "931ca233826ff9dacd889967365db1cde9ed8402eb553de2a3b9d58b6ff1098d",
            "farm-staking": "6dc7c587b2cc4b177a192b709c092f3752b3dcf9ce1b484e69fe64dc333a9e0a",
            "farm-staking-proxy": "56468a6ae726693a71edcf96cf44673466dd980412388e1e4b073a0b4ee592d7",
            "farm-with-locked-rewards": "437b2a665e643b5885cf50ee865c467371ca6faa20a8ff14a4b626c775f49971",
            "fees-collector": "c46767232cd8551f8b0f4aa94dc419ddefc13eaaa5aa4b422749a300621149f3",
            "governance": "959388eadaf71ff106252c601ae2767a5c62d7bd0ab119381c28dc679975685e",
            "governance-v2": "786a6cf08f1d961814ebb062f149c9a943d39d7db93d8f53aa1fc42b8e652f49",
            "lkmex-transfer": "995311e0dbd75ddc51a5c0c71ab896245c996b9b3993d3118a153bfb5531e123",
            "locked-token-wrapper": "f9ee63d96163e3fac52a164c76d91c85fd77968393a50d4a96a7080e648d0a6c",
            "metabonding-staking": "f508c5643b3d5f5e79b68762a9ca9e247c753acd305a29009328c5ec5d153bdd",
            "pair": "f3f08ebd758fada871c113c18017d9761f157d00b19c4d3beaba530e6c53afc2",
            "pair-mock": "a54495375db964cf924391433605d602940174d4d28111b89b8689564d90e662",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "6df095b15272b189c2e7b3628a21e17c1a6b26e5ed03e9a7bddac61be29d162f",
            "proxy-deployer": "5108e7419546872d235f0b7db5e01c5d04fec243bfa599c666629ead13bab0aa",
            "proxy_dex": "988dd8b632e1b4bb9b43e5636ef4c363dd4066186f64f6f783f9cd043aa906c1",
            "router": "c21ab56ef24b0719c101677170557e5aa61e1d17c1052ed7b2290cb26a5bdcd6",
            "simple-lock": "303290b7a08b091c29315dd6979c1f745fc05467467d7de64e252592074890a7",
            "simple-lock-whitelist": "c576c6106234e5f7978efb1885afe36c5d6da6a13c12b459fd7fe95967646d13",
            "token-unstake": "463e49892f64726450d0df5ab4ba26559ad882525ce5e93173a26fde8437266e",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.1.0"
    ),
    PreviousBuild(
        name="e.2",
        project_zip_url="https://github.com/multiversx/mx-exchange-sc/archive/refs/heads/reproducible-v2.0-rc6.zip",
        project_path_adjustment="mx-exchange-sc-reproducible-v2.0-rc6",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "distribution": "17a30ad44291af84f6dbd84fdaf0a9a56ed7145d544c54fd74088bb544c4f98f",
            "energy-factory": "62d60c8dec649614dd9cf04fb20b884c7658b12759fa14bf7e9c7be3880a5edd",
            "energy-factory-mock": "83b2f26a52e3fe74953f2a8cfd81f169664a4e59dae4e5d5bb1d89956fd81d43",
            "energy-update": "8523bf84ac56626c70c31342487445bf8123e3ef5f906dcb39e8b5f16c4145b7",
            "factory": "df06465b651594605466e817bfe9d8d7c68eef0f87df4a8d3266bcfb1bef6d83",
            "farm": "69f95b5f9a4d5b6bb101d5d2cf7495264a4d04de2b36653e0c8088cf6fad492a",
            "farm-staking": "ca0a8ceed8b8807b0fb078153c15167a3a235a61a76edc5023dfcacae0446125",
            "farm-staking-proxy": "56468a6ae726693a71edcf96cf44673466dd980412388e1e4b073a0b4ee592d7",
            "farm-with-locked-rewards": "c18d75ea788ece457788ad8849722a42dd4a12e6e23ab87f0cdffcc0116b61be",
            "fees-collector": "c46767232cd8551f8b0f4aa94dc419ddefc13eaaa5aa4b422749a300621149f3",
            "governance": "959388eadaf71ff106252c601ae2767a5c62d7bd0ab119381c28dc679975685e",
            "governance-v2": "786a6cf08f1d961814ebb062f149c9a943d39d7db93d8f53aa1fc42b8e652f49",
            "lkmex-transfer": "995311e0dbd75ddc51a5c0c71ab896245c996b9b3993d3118a153bfb5531e123",
            "locked-token-wrapper": "f9ee63d96163e3fac52a164c76d91c85fd77968393a50d4a96a7080e648d0a6c",
            "metabonding-staking": "f508c5643b3d5f5e79b68762a9ca9e247c753acd305a29009328c5ec5d153bdd",
            "pair": "23ce1e8910c105410b4a417153e4b38c550ab78b38b899ea786f0c78500caf21",
            "pair-mock": "a54495375db964cf924391433605d602940174d4d28111b89b8689564d90e662",
            "pause-all": "2ad8aa911555b41e397541eb46cd1a7fa87186146f8c2b295e3916303833f3cd",
            "price-discovery": "6df095b15272b189c2e7b3628a21e17c1a6b26e5ed03e9a7bddac61be29d162f",
            "proxy-deployer": "5108e7419546872d235f0b7db5e01c5d04fec243bfa599c666629ead13bab0aa",
            "proxy_dex": "988dd8b632e1b4bb9b43e5636ef4c363dd4066186f64f6f783f9cd043aa906c1",
            "router": "8429d332fb62b557b3549d3f509a55d6aff8638f53a5ee876358a831107102cf",
            "simple-lock": "303290b7a08b091c29315dd6979c1f745fc05467467d7de64e252592074890a7",
            "simple-lock-whitelist": "c576c6106234e5f7978efb1885afe36c5d6da6a13c12b459fd7fe95967646d13",
            "token-unstake": "463e49892f64726450d0df5ab4ba26559ad882525ce5e93173a26fde8437266e",
        },
        docker_image="multiversx/sdk-rust-contract-builder:v3.1.0"
    ),
    PreviousBuild(
        name="f.1",
        project_zip_url="https://github.com/multiversx/mx-nft-marketplace-sc/archive/refs/heads/reproducible-v2.0.1.zip",
        project_path_adjustment="mx-nft-marketplace-sc-reproducible-v2.0.1",
        packaged_src_url=None,
        contract_name=None,
        expected_code_hashes={
            "esdt-nft-marketplace": "aed8f014c914d2910cbb68b61adb757f8dbc8385842e717127482e1a66828bbe",
            "seller-contract-mock": "d3f42ae77ec60878ba62146a4209ef08a9400aecf083c96888ede316069985c0"
        },
        docker_image="multiversx/sdk-rust-contract-builder:v4.0.3"
    )
]


def main(cli_args: List[str]):
    shutil.rmtree(downloads_folder, ignore_errors=True)
    shutil.rmtree(extracted_folder, ignore_errors=True)
    shutil.rmtree(parent_output_folder, ignore_errors=True)

    downloads_folder.mkdir(parents=True, exist_ok=True)
    extracted_folder.mkdir(parents=True, exist_ok=True)
    cargo_target_dir.mkdir(parents=True, exist_ok=True)

    for build in builds:
        print("Reproducing build", build.name, "...")

        project_path, packaged_src_path = fetch_source_code(build)
        output_folder = parent_output_folder / build.name
        output_folder.mkdir(parents=True, exist_ok=True)

        if project_path and build.project_path_adjustment:
            project_path = project_path / build.project_path_adjustment

        run_docker(project_path, packaged_src_path, build.contract_name, build.docker_image, output_folder)

        artifacts_path = output_folder / "artifacts.json"
        artifacts_json = artifacts_path.read_text()
        artifacts = json.loads(artifacts_json)

        for contract_name, expected_code_hash in build.expected_code_hashs.items():
            print(f"For contract {contract_name}, expecting code hash {expected_code_hash} ...")
            codehash = artifacts[contract_name]["codehash"]
            if len(codehash) != 64:
                # It's an older image, "artifacts.json" contains a path towards the code hash, instead of the actual code hash
                codehash = Path(output_folder / contract_name / codehash).read_text().strip()

            if codehash != expected_code_hash:
                raise Exception(f"{build.name}: codehash mismatch for contract {contract_name}! Expected {expected_code_hash}, got {codehash}")
            print("OK, codehash matches!", codehash)


def fetch_source_code(build: PreviousBuild) -> Tuple[Optional[Path], Optional[Path]]:
    print("Fetching source code for", build.name, "...")

    if build.project_zip_url:
        downloaded_archive = downloads_folder / f"{build.name}.zip"
        extracted_project = extracted_folder / build.name
        urllib.request.urlretrieve(build.project_zip_url, downloaded_archive)
        shutil.unpack_archive(downloaded_archive, extracted_project)
        return extracted_project, None

    if build.packaged_src_url:
        downloaded_packaged_src = downloads_folder / f"{build.name}.json"
        urllib.request.urlretrieve(build.packaged_src_url, downloaded_packaged_src)
        return None, downloaded_packaged_src

    raise Exception("No source code provided")


def run_docker(
        project_path: Optional[Path],
        packaged_src_path: Optional[Path],
        contract_name: Optional[str],
        image: str,
        output_folder: Path,
):
    docker_mount_args: List[str] = ["--volume", f"{output_folder}:/output"]

    if project_path:
        docker_mount_args.extend(["--volume", f"{project_path}:/project"])

    if packaged_src_path:
        docker_mount_args.extend(["--volume", f"{packaged_src_path}:/packaged-src.json"])

    docker_mount_args += ["--volume", f"{cargo_target_dir}:/rust/cargo-target-dir"]

    docker_args = ["docker", "run"]
    docker_args += docker_mount_args
    docker_args += ["--user", f"{str(os.getuid())}:{str(os.getgid())}"]
    docker_args += ["--rm", image]

    entrypoint_args: List[str] = []

    if project_path:
        entrypoint_args.extend(["--project", "project"])

    if packaged_src_path:
        entrypoint_args.extend(["--packaged-src", "packaged-src.json"])

    if contract_name:
        entrypoint_args.extend(["--contract", contract_name])

    args = docker_args + entrypoint_args

    result = subprocess.run(args)
    return result.returncode


if __name__ == "__main__":
    main(sys.argv[1:])

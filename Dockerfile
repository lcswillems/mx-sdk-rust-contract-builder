FROM ubuntu:22.04

# Constants
ARG BUILDER_NAME="multiversx/sdk-rust-contract-builder:v4.1.3"
ARG VERSION_RUST="nightly-2022-10-16"
ARG VERSION_BINARYEN="105-1"
ARG VERSION_WABT="1.0.27-1"
ARG VERSION_SC_META="0.39.5"

# Temporary workaround. Default Ubuntu archive mirrors are down.
RUN sed -i 's|http://archive.ubuntu.com|http://de.archive.ubuntu.com|g' /etc/apt/sources.list

# Install dependencies
RUN apt-get update --fix-missing && apt-get install -y \
    wget \ 
    build-essential \
    python3.11 python-is-python3 python3-pip \
    binaryen=${VERSION_BINARYEN} \
    wabt=${VERSION_WABT}


RUN pip3 install toml==0.10.2 semver==3.0.0-dev.4

# Install rust
RUN wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    CARGO_HOME=/rust RUSTUP_HOME=/rust ./rustup.sh --verbose --default-toolchain ${VERSION_RUST} --profile minimal --target wasm32-unknown-unknown -y && \
    rm rustup.sh && \
    chmod -R 777 /rust && \
    rm -rf /rust/registry

# Install sc-tool
RUN PATH="/rust/bin:${PATH}" CARGO_HOME=/rust RUSTUP_HOME=/rust cargo install multiversx-sc-meta --version ${VERSION_SC_META} && \
    rm -rf /rust/registry

COPY "multiversx_sdk_rust_contract_builder" "/multiversx_sdk_rust_contract_builder"

ENV PATH="/rust/bin:${PATH}"
ENV CARGO_HOME="/rust"
ENV RUSTUP_HOME="/rust"
ENV PYTHONPATH=/
ENV BUILD_METADATA_BUILDER_NAME=${BUILDER_NAME}
ENV BUILD_METADATA_VERSION_RUST=${VERSION_RUST}
ENV BUILD_METADATA_VERSION_BINARYEN=${VERSION_BINARYEN}
ENV BUILD_METADATA_VERSION_WABT=${VERSION_WABT}
ENV BUILD_METADATA_VERSION_SC_META=${VERSION_SC_META}

# Additional arguments (must be provided at "docker run"):
# --project or --packaged-src
# --no-wasm-opt (optional)
# --build-root (optional)
ENTRYPOINT ["python", "/multiversx_sdk_rust_contract_builder/main.py", \
    "--output", "/output", \
    "--cargo-target-dir", "/rust/cargo-target-dir"]

LABEL frozen="yes"
LABEL rust=${VERSION_RUST}
LABEL wasm-opt-binaryen=${VERSION_BINARYEN}
LABEL wabt=${VERSION_WABT}
LABEL sc_meta=${VERSION_SC_META}

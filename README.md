# Porter

[![CodeFactor](https://www.codefactor.io/repository/github/dereknex/porter/badge)](https://www.codefactor.io/repository/github/dereknex/porter) [![codecov](https://codecov.io/gh/dereknex/porter/branch/main/graph/badge.svg?token=YCMJ0KX1RP)](https://codecov.io/gh/dereknex/porter)

Porter is a command-line utility that moves file or container images.

## How to use?

`python main.py --config=<CONFIG_PATH>`

## Example configuration

```yaml
auto_clean: true
local_path: temp/
inputs:
  - name: http
    kind: http
  - name: docker
    kind: docker
outputs:
  - name: docker
    kind: docker
  - name: kubernetes
    kind: s3
    bucket: kubernetes
    access_key: foo
    access_key_secret: bar12345
    endpoint: localhost:9000
    secure: false
tasks:
  - name: kubectl
    input:
      name: http
      url: https://storage.googleapis.com/kubernetes-release/release/{{ version }}/bin/linux/{{ image_arch }}/kubectl
      sha256sum: '{{ sha256sum }}'
    output:
      name: kubernetes
      remote_prefix: '{{ version }}/linux/{{ image_arch }}/kubectl'
    with_items:
      - title: v1.21.3-arm
        version: v1.21.3
        sha256sum: 603b6e57c5546c079faee6b606014e83b95ea076146fbf73329f3069968f83bf
        image_arch: arm
      - title: v1.21.2-arm
        version: v1.21.2
        sha256sum: 898c2cd54b651873a8fb18bcb0792eb4772a78f845d758fa9b0eee278aede869
        image_arch: arm
  - name: kubernetes-source
    input:
      name: http
      url: https://github.com/kubernetes/kubernetes/releases/download/{{ version }}/kubernetes.tar.gz
      sha256sum: '{{ sha256sum }}'
    output:
      name: kubernetes
      remote_prefix: '{{ version }}/kubernetes.tar.gz'
    with_items:
      - title: v1.21.4
        version: v1.21.4
        sha256sum: 4c9b918958276ca01a5c93925c8954c8ac343a8bbfc4afa0f8391c95e9bfe727
      - title: v1.20.10
        version: v1.20.10
        sha256sum: a01b54ad1bf4162073c7d51a607e60091b6f053522aaa01334f231b83e7aca25
  - name: kube-proxy
    input:
      name: docker
      image: k8s.gcr.io/kube-proxy:{{tag}}
    output:
      name: docker
      image: localhost:5000/kube-proxy:{{tag}}
    with_items:
      - title: v1.21.4
        tag: v1.21.4
        platform: amd64
```

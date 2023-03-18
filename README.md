# hello-world-demo

This repository contains a simple Flask App that displays 'Hello, World!' and can be deployed in Minikube.

## Pre-Requisite / Dependencies

You will need the following to launch the App:

  - Python 3 (and `pip`)
  - [Minikube](https://minikube.sigs.k8s.io/docs/) 

### Optional

The following is a list of tools that are not required, but helpful to have:

  - [Helm](https://helm.sh/) - Used to deploy in to Minikube using the included Helm Chart
  - [Taskfile](https://taskfile.dev/) - Run tasks in the included `Taskfile.yaml`

---
## Get started

  There are two ways to deploy the `hello-world` app in to Minikube, you can deploy manually or you can using `Taskfile`.

  Both ways follow the same steps, however using `Taskfile`automates the process.

### Manually
1. Ensure Minikube cluster is up and running with ingress addon enabled: 

    ```shell
    $ minikube start
    $ minikube addons enable ingress
    ```

2. Build container image and ensure that it's loaded in to Minikube cluster: 

    ```shell
    minikube image build -t 127.0.0.1/hello-world-demo:local .
    ```
3. Deploy in to Minikube:

    ```shell
    $ minikube kubectl -- apply -f ./static-deploy.yaml
    $ minikube service -n ingress-nginx ingress-nginx-controller --url | head -1
    ```
    You will see URL displayed, browsing to that link should display the App.

    _Note: HTTP `Host` must be `static-hello.localdomain` when making the request, or add an entry to `/etc/hosts`_

### Manually Using Helm

1. Ensure Minikube cluster is up and running:

    ```shell
    $ minikube start
    ```

2. To be safe, set `KUBECONFIG` path:

    ```shell
    $ export KUBECONFIG=${PWD}/.kubeconfig
    $ minikube update-context
    ```

3. Build container image and ensure that it's loaded in to Minikube cluster: 

    ```shell
    minikube image build -t 127.0.0.1/hello-world-demo:local .
    ```

4. Deploy using Helm:

    ```shell
    $ helm upgrade --install \
        -n hello-world \
        --create-namespace \
        -f helm/hello-world/deploy-values.yaml \
        hello-world \
        helm/hello-world/
    
    $ minikube service -n ingress-nginx ingress-nginx-controller --url | head -1
    ```
    You will see URL displayed, browsing to that link should display the App.

    _Note: HTTP `Host` must be `hello.localdomain` when making the request, or add an entry to `/etc/hosts`_

### Using Taskfile

Simply run the either of the following:

```shell
task helm-install # To deploy using Helm
```
Or
```shell
task minikube-helloworld-deploy # To deploy without using Helm
```

The default task will run `helm-install`, so if you have `helm` installed, you can also just run `task`

A list of tasks can be shown by running `task -l`:

```shell
$ task -l
task: Available tasks for this project:
* build-image:                      Build Container image
* helm-install:                     Deploy Hello World app using Helm
* minikube-helloworld-deploy:       Deploy Hello World App using minikube
* minikube-launch:                  Launch Minikube cluster with Docker driver
* python-test:                      Lint and test Python code
```
---
## The Flask App

The app is very simple "Hello, World!" example app, but does provide a API endpoint that allows the user to customise the greeting.

### Endpoints

_Note:_ Output can be formatted in json by appending `?output=json` to the request

- `/`     
    
    ```shell
    # Regular Output
    $ curl -H 'Host: static-hello.localdomain' http://127.0.0.1:30269/
    Hello, World!
    
    # Output in JSON
    $ curl -H 'Host: static-hello.localdomain' http://127.0.0.1:30269/?output=json
    {"name":"World","output":"Hello, World!"}
    ```

-  `/hello/<name>`
    ```shell
    # Regular Output
    $ curl -H 'Host: static-hello.localdomain' http://127.0.0.1:30269/hello/yasser
    Hello, Yasser!

    # Output in JSON
    $ curl -H 'Host: static-hello.localdomain' http://127.0.0.1:30269/hello/yasser?output=json
    {"name":"Yasser","output":"Hello, Yasser!"}
    ```
---

## Development

Work should be undertaken in a virtual env to prevent causing any conflicts with your system installation.

Once you are running in a virtual env, install the needed pip modules:

```shell
$ pip install -r dev-requirements.txt
```

The code conforms to PEP8 style guide and you can use `pycodestyle` to check:

```shell
$ pycodestyle src/
```

Tests are also provided in `src/tests`, to run tests:

```shell
$ pytest --no-header src/
====================================================================================== test session starts ======================================================================================
collected 4 items

src/tests/test_endpoint.py ....                                                                                                                                                           [100%]

======================================================================================= 4 passed in 0.07s =======================================================================================
```
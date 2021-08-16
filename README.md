# 2Py

Expertimenting the exploitation of [JPype](https://jpype.readthedocs.io) to port [2P-Kt](https://github.com/tuProlog/2p-kt) on Python.

## Introduction

Long description of the project

## How to do stuff

### Prerequisites

1. Install Python 3 (look into the `.python-version` to know the exact version)
    * I suggest using [Pyenv](https://github.com/pyenv/pyenv) to easily handle multiple Python versions on the same machine
    * Ensure PIP works fine

2. Install Java (JDK preferred), and **ensure the `JAVA_HOME` variable is correctly set**

3. Ensure Java and Python are both either 64bit or 32bit

4. Restore Python dependencies via PIP, by running:
    ```bash
    pip install -r requirements.txt
    ```

5. Restore JVM dependencies via `download-jars.sh`, by running:
    ```bash
    ./download-jars.sh
    ```

### How to use project

- Eventually, as a library. For the moment, as a demo.

- Run the `main.py` file to see a demo:
    ```bash
    python main.py
    ```

    Expected outcome should be something like the following:
    ```
    DEBUG:root:Started JVM vX.Y.Z
    DEBUG:root:Configure Kt-specific extensions
    DEBUG:root:Using 2P-Kt v0.18.2
    DEBUG:root:Loaded JVM classes from it.unibo.tuprolog.core.*
    DEBUG:root:Loaded JVM classes from it.unibo.tuprolog.solve.*
    DEBUG:root:Loaded JVM classes from it.unibo.tuprolog.theory.parsing.*
    Yes(query=grandparent(X_3, Y_2), substitution={X_3=charles2, Y_2=james1})
    Yes(query=grandparent(X_3, Y_2), substitution={X_3=catherine, Y_2=james1})
    Yes(query=grandparent(X_3, Y_2), substitution={X_3=james2, Y_2=james1})
    Yes(query=grandparent(X_3, Y_2), substitution={X_3=sophia, Y_2=james1})
    Yes(query=grandparent(X_3, Y_2), substitution={X_3=george1, Y_2=elizabeth})
    ```


### How to develop the project

TBD

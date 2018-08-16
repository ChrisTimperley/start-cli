# start-cli

Provides a command-line interface to START

## Commands

To sanity check the test suite behaviour of a given scenario:

```
$ startcli repair validate ~/start/scenarios/AIS-Scenario1/scenario.config
```

To attempt to find a repair for a given scenario:

```
$ startcli repair repair ~/start/scenarios/AIS-Scenario1/scenario.config
```

To perform static analysis on the source code for a given scenario:

```
$ startcli repair analyze ~/start/scenarios/AIS-Scenario1/scenario.config
$ cat analysis.json
```

To localise the fault for a given scenario and to compute its coverage
information:

```
$ startcli repair localize ~/start/scenarios/AIS-Scenario1/scenario.config
$ cat coverage.json
```

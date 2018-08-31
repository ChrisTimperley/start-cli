# START Command-Line Interface

Provides a command-line interface to START.

## Commands

To obtain a list of commands and to learn more about a given command:

```
$ start-cli --help
```

Sanity checking can be used to ensure that the test suite for a given
scenario behaves as expected (i.e., it fails when the attack is performed
but passes when it is not). To perform sanity checking:

```
$ start-cli validate ~/start/scenarios/AIS-Scenario1/scenario.config
```

To attempt to find a repair for a given scenario:

```
$ start-cli repair ~/start/scenarios/AIS-Scenario1/scenario.config
```

To precompute a static analysis of the source code for a given scenario:

```
$ start-cli analyze ~/start/scenarios/AIS-Scenario1/scenario.config
```

To precompute the line coverage information for a given scenario:

```
$ start-cli coverage ~/start/scenarios/AIS-Scenario1/scenario.config
```

To precompute the fault localization for a given scenario:

```
$ start-cli localize ~/start/scenarios/AIS-Scenario1/scenario.config
```

## Debugging

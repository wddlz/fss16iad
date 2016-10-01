#Reading 5, Team C
* [DynaMoth: dynamic code synthesis for automatic program repair](http://dl.acm.org/citation.cfm?id=2896931)

1. *Reading*
  + 	Thomas Durieux and Martin Monperrus. 2016. DynaMoth: dynamic code synthesis for automatic program repair . AST 2016 Proceedings of the 11th International Workshop on Automation of Software Test.
2. *Keywords*

  1. **Nopol**:Nopol is a repair system that repairs Java code using code synthesis and uses DynaMoth as synthesis engine.
  2. **Fault Classes**:Classes of bugs where fault occurs and the sytem Nopol targets.
  3. **Evaluated-Expression**:denoted as EEXP (c) is a pair e, v where e is a valid Java expression and v the value of the Java expression in a specific runtime context c.
  4. **Test-suite-based Repair**: Test suite based repair uses a test suite as the specification of the correct behavior of the program.
  5. **Angelic Value Mining**: The angelic value mining step determines the required value of the buggy boolean expression to make the failing test cases to pass.

3. *Notes (4 of 19)*
  1. **Motivational statements**: The paper describes implementation and details synthesis engine called as DynaMoth for Nopol which initially used SMTSynth and now DynaMoth .DynaMoth uses dynamic exploration of tentative expressions based on Angelic Value Mining to collect runtime context.The evaluation shows that Nopol with DynaMoth is capable of repairing bugs that have never been
repaired so far.

  2. **Hypotheses**:DynaMoth's main design goal is to be capable to synthesize patches with complex operators and those involving method calls with parameters. Synthesizing method calls would yield huge search space.

  3. **Related work**: CodeHint is a closest synthesis engine as DynaMoth, which synthesizes Java code from runtime data inside the development environment by using JRE runtime debug interface to collect runtime data and call methods. However major difference between CodeHint and DynaMoth would be that CodeHint has a goal to help developers whereas DynaMoth tries to achieve automatic repair.Also, CodeHint synthesize an expression for single runtime context whereas DynaMoth has to generate expression that is valid for many runtime contexts at same time which increases the DynaMoth's complexity in terms of synthesis engine.
  Other related work would be GenProg which uses genetic algorithm implemented in C to copy existing code in the program instead of synthesizing code. SemFix is another such tool that uses symbolic execution for fixing assignment and conditions, which uses same algorithm as SMTSynth for synthesis with which the paper compares in detail.

  4. **Future work**: The authors of the paper in future plan to implement additional optimizations, mostly to address the combinatorial explosion of the search space caused by method accepting many arguments. In additional to it, the paper mentions using many candidate Evaluated-Expressions to be used as parameters.

4. *Needs improvement*
  1. Fault Classes are limited to only two in this paper, buggy if and missing preconditions. The paper does not mention if the fault classes can be added or a discussion about how adding fault classes could cause implications on current evaluations.
  2. The paper says that initially SMTSynth was used as a synthesis engine and now evaluated with DynaMoth, and SMTSynth and Dynamoth are both complementary . This would drastically reduce automatic bug repairs done since new method might fix new bugs but would still require previous method to do better fix repair. There is not discussion in the paper that would point to such merged system with both techniques.
  3. The paper mentions the execution time of DynaMoth is comparable to that of SMTSynth for all bugs but slower when considering the fixed bugs and average repair time remains acceptable for classical repair scenarios. However,the paper design does not mention what acceptable or unacceptable is.

5. *Connection to other papers*
  1. **Connection to GZoltar**: This paper uses GZoltar's library for fault localization. The Implementation of DynaMoth includes the Gzoltar library for localization of suspicious statement and then proceeds to explore the space of all possible expressions at the give suspicious statement.

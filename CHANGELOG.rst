
1.3.0
-----

Pull Requests:

- @ryaneverett: #134; Pass taskrc via environment variable to subprocess.
- @ryaneverett: #131; Adds testing for Python 3.7 and 3.8
- @gdeterez: #130; Fix error raised when taskwarrior is not installed.
- @bergercookie: #124; Fix bug on deletion of completed task; disable
  confirmation for recurring tasks; fix bug in numeric deserialization.
- @matt-snider: #121; Fixes bug in which UUIDs were improperly parsed
  when creating recurring tasks.
- @yonk42: #116; Fix a bug in which configuration values having an equal
  sign in their value would be improperly parsed.

Mechanical:

- Switched from nose to pytest.
- Switched from travis.ci to github actions.

Deprecated:

- Dropped automated testing for Python 3.4.

1.2.0
-----

Pull Requests

- (@ryansb)         #103, Strip form feed/bell chars
  https://github.com/ralphbean/taskw/pull/103
- (@ryansb)         #105, Also remove literal escape characters `^[`
  https://github.com/ralphbean/taskw/pull/105
- (@ryansb)         #104, Use the `errno` library instead of string matching error text
  https://github.com/ralphbean/taskw/pull/104
- (@ryneeverett)    #107, Travis Testing Improvements
  https://github.com/ralphbean/taskw/pull/107
- (@ryneeverett)    #108, Downgrade string coercion from warning to debug.
  https://github.com/ralphbean/taskw/pull/108
- (@gdetrez)        #109, Fix bugwarrior issue #393
  https://github.com/ralphbean/taskw/pull/109

Commits

- ac720a5f2 Test against beta2.
  https://github.com/ralphbean/taskw/commit/ac720a5f2
- de5fa87d9 task 2.5.0 is out!
  https://github.com/ralphbean/taskw/commit/de5fa87d9
- 11cdab50f Use kitchen in the most dire of circumstances.
  https://github.com/ralphbean/taskw/commit/11cdab50f
- 36406c6d5 All hail 2.5.1.
  https://github.com/ralphbean/taskw/commit/36406c6d5
- 00ea026aa Strip form feed/bell chars
  https://github.com/ralphbean/taskw/commit/00ea026aa
- c97ed88c1 Use the `errno` library instead of string matching error text
  https://github.com/ralphbean/taskw/commit/c97ed88c1
- 359543f37 Move import
  https://github.com/ralphbean/taskw/commit/359543f37
- 1bacb40bf Also remove literal escape characters `^[`
  https://github.com/ralphbean/taskw/commit/1bacb40bf
- 8d86fc538 Downgrade string coercion from warning to debug.
  https://github.com/ralphbean/taskw/commit/8d86fc538
- bae210000 Fix the v2.4.4 tag name in travis.yml.
  https://github.com/ralphbean/taskw/commit/bae210000
- fc41a5917 Upgrade travis to ubuntu trusty.
  https://github.com/ralphbean/taskw/commit/fc41a5917
- 64574e276 Run Travis against taskwarrior 2.5.x series.
  https://github.com/ralphbean/taskw/commit/64574e276
- 1b19f66eb Run tests against python3.5.
  https://github.com/ralphbean/taskw/commit/1b19f66eb
- 74b778552 Remove taskwarrior 2.4.3-2.4.4 from Travis matrix.
  https://github.com/ralphbean/taskw/commit/74b778552
- c9c2e75c1 Run on py35 now.
  https://github.com/ralphbean/taskw/commit/c9c2e75c1
- 840613288 Add a function to clean control characters
  https://github.com/ralphbean/taskw/commit/840613288
- 32a87235f Clean control characters in command
  https://github.com/ralphbean/taskw/commit/32a87235f

1.1.0
-----

Primarily: 

- Compatibility with task-2.5.0.beta1 `91cc20f96 <https://github.com/ralphbean/taskw/commit/91cc20f96b50a4ebe72c22fb3b498b9b3e8a97f9>`_

Also:

- Improvements to dependency behavior. `a9f716456 <https://github.com/ralphbean/taskw/commit/a9f71645676f42852789b791ba42a6314227a7e0>`_
- Shuffle some things in Task just to make classmethods easier. `938171e3b <https://github.com/ralphbean/taskw/commit/938171e3bd6d8e03522fbe072ac24146a43b7a7c>`_
- Add test. `3c494c1e4 <https://github.com/ralphbean/taskw/commit/3c494c1e4479c577127f95ce858991569eb5a008>`_
- Make .load_config() work as expected. `971ddc6b3 <https://github.com/ralphbean/taskw/commit/971ddc6b368d9a3e9f5f9c9c0fc52dab89ced13d>`_
- Merge pull request #93 from ralphbean/feature/nested-config `a8301a7cc <https://github.com/ralphbean/taskw/commit/a8301a7ccdf0ab79625ff6950a4fd54dade90206>`_
- Merge pull request #92 from ralphbean/feature/recursive-tasks `57939f4c4 <https://github.com/ralphbean/taskw/commit/57939f4c46b5841e716dc44bf847e47ad7cabf56>`_
- Check TASKRC environment var, default to ~/.taskrc `03b908bce <https://github.com/ralphbean/taskw/commit/03b908bcedb0bc36d4c8f5f9b1fc62271296417b>`_
- Merge pull request #95 from khaeru/develop `17133f22f <https://github.com/ralphbean/taskw/commit/17133f22feed0ef002ecc1b3658717eeb933e9b0>`_
- Raise a more descriptive error `02b9fa5db <https://github.com/ralphbean/taskw/commit/02b9fa5dbd6fd56b453af4a1f04afc166571cf73>`_
- Merge pull request #97 from ralphbean/feature/more-descriptive-error `69e63c04e <https://github.com/ralphbean/taskw/commit/69e63c04ee3dfe59dc502cf7bf8aa9daf849e0ed>`_
- Test against task-2.4.2 also. `310c2e473 <https://github.com/ralphbean/taskw/commit/310c2e47343d7933829032d788dc83b21aaa2466>`_
- Expand tox and travis to test against the latest taskwarrior release. `e2df21780 <https://github.com/ralphbean/taskw/commit/e2df2178081f3f0f21c722475739d0d876027cf1>`_

1.0.3
-----

- Replace attr.is:value queries with attr == "value". `417928c8f <https://github.com/ralphbean/taskw/commit/417928c8f297fed4091592c55c17ba5e66de17fb>`_
- Merge pull request #91 from ralphbean/feature/is-to-equals `55afe8db4 <https://github.com/ralphbean/taskw/commit/55afe8db4f8aba598a7fb6cf77898ff6b2356519>`_
- Use the 'release build' just to make things faster `3b10aee66 <https://github.com/ralphbean/taskw/commit/3b10aee661808d8cf3cb034c5a5bf9e8568ff4a4>`_
- Test against task-2.4.1.  It is out! `4b170808d <https://github.com/ralphbean/taskw/commit/4b170808df90b04e224a6c32de60ae0557b5df4f>`_

1.0.2
-----

- This one too. `72d61ee33 <https://github.com/ralphbean/taskw/commit/72d61ee334c183a7e819c954099a3690bb9a7aa6>`_

1.0.1
-----

- Ding this req. `2d9c546eb <https://github.com/ralphbean/taskw/commit/2d9c546eb9da57a75468c479d7abb15047a0c793>`_

1.0.0
-----

- Don't encode characters nested within queries. `0e0869c9c <https://github.com/ralphbean/taskw/commit/0e0869c9c6034770d1e833bae5784d63d4cd5047>`_
- Parse uuids from "task add" output when necessary. `6817eb027 <https://github.com/ralphbean/taskw/commit/6817eb0273ceb75870de742b29ec07db98aa7cf0>`_
- Present args correctly to the taskwarrior parser. `4e11ad049 <https://github.com/ralphbean/taskw/commit/4e11ad049566db690823721201c7b480bea4ab0d>`_
- Check specifically for this to reduce confusion in test failure output. `92633f4cb <https://github.com/ralphbean/taskw/commit/92633f4cb78b2f0a78d5773b12b0a3a56c497f38>`_
- Dance around this. `1f83582b9 <https://github.com/ralphbean/taskw/commit/1f83582b93c0b53c02f4c12c9d316ebebf686995>`_
- Strip out argued uuid if on taskwarrior-2.4 or later. `ad51ab62b <https://github.com/ralphbean/taskw/commit/ad51ab62b560f9b5bf3778966de14ae3746a1a98>`_
- Comment out failing tests due to bugs in taskwarrior-2.4 and later. `28f71ebf5 <https://github.com/ralphbean/taskw/commit/28f71ebf574d66b4a2053352e9d1e26cd496720f>`_
- Corrected syntax in completing tasks example `d27eb9557 <https://github.com/ralphbean/taskw/commit/d27eb9557a2180ad499442fba415e9792c338625>`_
- Added retrieve, update and delete examples `843a68d07 <https://github.com/ralphbean/taskw/commit/843a68d07ee1cf6c7d99d756cc4a2900ec631225>`_
- Corrected the section on updating tasks `57c33a799 <https://github.com/ralphbean/taskw/commit/57c33a799b73febaf86227e27e71c747b4aaeaab>`_
- Merge pull request #69 from countermeasure/readme `3ec674957 <https://github.com/ralphbean/taskw/commit/3ec6749576ac5a40f4c57a04fa9c0069afabbb15>`_
- Added a test for addition of a numeric UDA `4d21be9e7 <https://github.com/ralphbean/taskw/commit/4d21be9e73b1d0d8338327f2ee528fc182a0c047>`_
- Added failing tests for removal of UDAs `d3c623319 <https://github.com/ralphbean/taskw/commit/d3c6233196760a6fcfe5bf575ea49b1f1800cb9f>`_
- Allow numeric fields to accept value of None `d92d60e00 <https://github.com/ralphbean/taskw/commit/d92d60e00c44ecce9a0ec567be21ab887d3bdfe7>`_
- Allow string fields to accept value of None `e04045959 <https://github.com/ralphbean/taskw/commit/e0404595996c1ae957862a02d798ee38de414c38>`_
- Adding all these tests back in to check out the task-2.4.0.beta3 release. `cd2dda7b5 <https://github.com/ralphbean/taskw/commit/cd2dda7b59ad4674bb62c6dc5d47f462d68e7bc3>`_
- Do not swallow KeyError and return field-specific null values for known fields. `b1dc1eab7 <https://github.com/ralphbean/taskw/commit/b1dc1eab741a5aacc279e3e40f160e60506d2ce1>`_
- test: set the timezone to UTC when adding a task `9323d6755 <https://github.com/ralphbean/taskw/commit/9323d6755cebcbde36c0d8fbe10847bce1329f9d>`_
- Merge pull request #76 from dev-zero/develop `717e65f18 <https://github.com/ralphbean/taskw/commit/717e65f183ac627a3d80e2f66e68167e9c8ae3dc>`_
- DirtyableDict should be a subclass of dict, not list. `884346444 <https://github.com/ralphbean/taskw/commit/884346444a8e061092f1d9425e64affdf4da705d>`_
- Simplifications and fixes to `Task.get` and `Task.__setitem__` to reduce surprises. `4c579ce25 <https://github.com/ralphbean/taskw/commit/4c579ce2539849e2ad11dfe3436718df2f4a1218>`_
- Get the DirectDB method to delete values correctly. `cc1d78a34 <https://github.com/ralphbean/taskw/commit/cc1d78a341553384c4e80c0c4b533683c4c0bf03>`_
- Remove unused import. `941001d1d <https://github.com/ralphbean/taskw/commit/941001d1dcf7c976fa4713d5ea602ee9f8922b9b>`_
- Remove test we decided to jettison at the end of #70. `304c1af94 <https://github.com/ralphbean/taskw/commit/304c1af94d3ddc4e34e453daf0ee4beb3edadfc2>`_
- Merge branch 'uda_handling_alterations' into develop `032c00e70 <https://github.com/ralphbean/taskw/commit/032c00e70fcdf448cb891740c113f3c9019a1d27>`_
- Add failing test case for `?` escaping `bc6eb5ab3 <https://github.com/ralphbean/taskw/commit/bc6eb5ab37587bfa23331c1c87f8bb3b9375b029>`_
- Do not quote `?` when used with an exact match. `d29af8436 <https://github.com/ralphbean/taskw/commit/d29af84360086ed17fb36677b1ab4b616e65fd01>`_
- Merge pull request #78 from djmitche/issue77 `e7be645c1 <https://github.com/ralphbean/taskw/commit/e7be645c1c55190fc2dffda5af4ed65ab6079569>`_
- py3 fix. `fc16948ea <https://github.com/ralphbean/taskw/commit/fc16948eafff997b143752b535d415388db1b084>`_
- Use rc.dependency.confirmation=no when running task. `03cee7ae3 <https://github.com/ralphbean/taskw/commit/03cee7ae32e8a8b5a2dfdcc63b2da8e49b10d6cf>`_
- Squash the (hopefully) last encoding bug w.r.t. task-2.4.0 `14ff33d0c <https://github.com/ralphbean/taskw/commit/14ff33d0c15aea4f38ff74e81243fd893140bc54>`_
- Issue 72: Instruct travis-ci to test taskw using multiple taskwarrior versions. `8a5efc3cf <https://github.com/ralphbean/taskw/commit/8a5efc3cfe8eed37f471a9c2d3235944fdd44cc3>`_
- Issue 72: Install some required packages. `7489ca567 <https://github.com/ralphbean/taskw/commit/7489ca567603e1343d8da32e19d5878a451d21eb>`_
- Issue 72: Use sudo for task installation. `cf68420a4 <https://github.com/ralphbean/taskw/commit/cf68420a414ab843222887f46fcaa8efbfd98458>`_
- Issue 72: Use sudo for installing packages; of course. `9a11bb9e9 <https://github.com/ralphbean/taskw/commit/9a11bb9e91a67f8610fa77db3aca7486329295df>`_
- Issue 72: Switch back to package directory after installing taskwarrior. `11bc2fe12 <https://github.com/ralphbean/taskw/commit/11bc2fe1292c1fdcdfd7af3f2be221f8a065d720>`_
- Merge pull request #82 from coddingtonbear/72_test_under_multiple_taskwarrior_versions `c8edd25b1 <https://github.com/ralphbean/taskw/commit/c8edd25b1e33a5b4f55890a05b158221b6bb5b44>`_
- Issue 83: Adding basic tox testing framework for local testing in multiple environments on each taskwarrior version. `e4a3d6977 <https://github.com/ralphbean/taskw/commit/e4a3d6977feb291ee4742e79517fc5563a5c5d2c>`_
- Issue 85: Generate a list of keys prior to beginning iteration. `e7ed3ccb1 <https://github.com/ralphbean/taskw/commit/e7ed3ccb127ff98f9e5587569dab4fa9c2545d69>`_
- Issue 83: Allow passing positional args to py.test (so you can run one test at a time, for example). `e0df14111 <https://github.com/ralphbean/taskw/commit/e0df14111feeae52261ba0efadec22611605141c>`_
- Merge pull request #86 from ralphbean/85_fix_python3k_key_iteration `d3339df88 <https://github.com/ralphbean/taskw/commit/d3339df88130348336b79580f1d43e6d7e7dabb2>`_
- Issue 83: Use nose for tests rather than py.test. `72c1aee03 <https://github.com/ralphbean/taskw/commit/72c1aee036cb38d27ced98b3d97445184c7b3a34>`_
- Merge branch 'develop' into feature/task-2.4 `55090cd9f <https://github.com/ralphbean/taskw/commit/55090cd9ffbaf9de4d8f22259b5ca4cc7e6467d2>`_
- Apply the unicode-sandwich principle. `05e4e830d <https://github.com/ralphbean/taskw/commit/05e4e830d7d4744d36b49bda2d0fee36c956434e>`_
- Add python-3.4 to the mix `7f0b836ba <https://github.com/ralphbean/taskw/commit/7f0b836ba8c59aaf384c3ab0a16a8b847e4ccdd5>`_
- Merge branch '83_tox_testing' into feature/task-2.4 `bbd7484f9 <https://github.com/ralphbean/taskw/commit/bbd7484f98007196d50906e42f2ddc34540d59b3>`_
- Fix py3 iterator behavior. `058eed0db <https://github.com/ralphbean/taskw/commit/058eed0db98e343980e36a1dd7f0ac53c9a96032>`_
- Add python-3.4 to our travis matrix. `e2a13f5d1 <https://github.com/ralphbean/taskw/commit/e2a13f5d1f6391c6a8f5debd8e4d031184a9e806>`_
- Encode sub-queries differently for different versions of taskwarrior. `01682adda <https://github.com/ralphbean/taskw/commit/01682adda1018f20c6eaa94b0be85933dd76d8e5>`_
- I'm not sure how this test ever passed, so I'm going to punt. `af343d230 <https://github.com/ralphbean/taskw/commit/af343d23048b20c367ea07f41d75285347d09b21>`_
- Add taskwarrior-2.4.1 in there. `17e880af2 <https://github.com/ralphbean/taskw/commit/17e880af2506b590cd1219b637392c7d8ff15403>`_
- Throw v2.4.1 in here too. `a5dd24c9a <https://github.com/ralphbean/taskw/commit/a5dd24c9af31ee019c9473532a4931df03f17f0c>`_
- Since this hasn't been released yet, use the branch name. `f93bf019f <https://github.com/ralphbean/taskw/commit/f93bf019f8a6238c8b5b999192ce9f420d2c4e72>`_
- That stuff didn't seem to work.  No big.  Release coming soon. `875776aa5 <https://github.com/ralphbean/taskw/commit/875776aa507bf4358d9cecd05a339071db6f656d>`_
- Merge pull request #68 from ralphbean/feature/task-2.4 `934aac027 <https://github.com/ralphbean/taskw/commit/934aac0272f4dfdb33ef6538c24b48ee435cbc88>`_
- Adding test that ensures we can store and retrieve values by UDA. `35996b295 <https://github.com/ralphbean/taskw/commit/35996b295185102b22b6bf8c774adf0ea6c51ab1>`_
- Adding another failed test for filtering of exported tasks. `722f7902b <https://github.com/ralphbean/taskw/commit/722f7902b7971aef613a4374f82e18924714b5e4>`_
- Adjust url search test to "work" `8432a2187 <https://github.com/ralphbean/taskw/commit/8432a218763b0956294b543e6edb8f06a84a34d4>`_
- Fix parenthetical subqueries as per @coddingtonbear's suggestion. `1387ed321 <https://github.com/ralphbean/taskw/commit/1387ed321682180bb9498b25e8f935ede891be3d>`_
- Fixes #88; Works around TW-1510 and TD-87. `db1cb64ad <https://github.com/ralphbean/taskw/commit/db1cb64ad4a378d8e30dd2a424402cd7037c50e2>`_
- Merge pull request #89 from coddingtonbear/88_circumvent_taskw_bug_wrt_empty_priority `2e32e446c <https://github.com/ralphbean/taskw/commit/2e32e446cc8b7c53cdcc6093f25736cf25ebb035>`_
- Move version string. `19dc59b2e <https://github.com/ralphbean/taskw/commit/19dc59b2e6c604a1d12d33be22d7b702dcb54680>`_

0.8.6
-----

- Turns out unittest2 is a backport from py2.7, not from py3.x. `4e605403c <https://github.com/ralphbean/taskw/commit/4e605403c6bc750ec1c330237b77b3f162536d8f>`_

0.8.5
-----

- Do not allow taskwarrior to attempt to parse the string passed-in to denotate. `e9716a2e9 <https://github.com/ralphbean/taskw/commit/e9716a2e9fabd4558c81055e4a378fb3190fa3d0>`_
- Merge pull request #64 from coddingtonbear/make_denotate_use_unparsed_string_too `43fc07638 <https://github.com/ralphbean/taskw/commit/43fc076388d74f548bfab1a8d9148293d5bca1a7>`_
- Decode the configuration file in UTF-8 mode. `fa491d7ce <https://github.com/ralphbean/taskw/commit/fa491d7ceefc764c328b7674fac95afb52dd9711>`_
- Fixing a bug in which, while merging two configuration trees, we encounter the dict/string problem.  Fixes #65. `477cc8b65 <https://github.com/ralphbean/taskw/commit/477cc8b6539599d783f7ae9750355ad24492ac3c>`_
- Merge pull request #66 from coddingtonbear/handle_unicode_configs `60218eef7 <https://github.com/ralphbean/taskw/commit/60218eef7942cb928b2462723067c52603c7046d>`_
- Merge pull request #67 from coddingtonbear/merge_trees_dict_nonsense `666d21ce5 <https://github.com/ralphbean/taskw/commit/666d21ce546873eab808c05b92d933b66a127b0b>`_
- 0.8.4 `fa0b386ee <https://github.com/ralphbean/taskw/commit/fa0b386ee191989e1942701a988dd53fa8dddb94>`_

0.8.3
-----

- Add failing test for annotation extension. `ee746dac9 <https://github.com/ralphbean/taskw/commit/ee746dac99bc277b50ce52715786a6eea1d28250>`_
- Add another failing test just to round it out. `aa637a950 <https://github.com/ralphbean/taskw/commit/aa637a950cffb1633349851a77db750630cf2723>`_
- Make Task object store newly fabricated attributes. `47d27c78f <https://github.com/ralphbean/taskw/commit/47d27c78f69840185dd0a629d5965f95190c45f5>`_

0.8.2
-----

- This works.. that's good. `d7163b28f <https://github.com/ralphbean/taskw/commit/d7163b28f51e37ea30f60cc0fad7e0188483fdd2>`_
- Refactoring task instance handling to support marshalling to and from python-specific (non-JSON) datatypes while retaining backward-compatible behavior. `1ed40ba95 <https://github.com/ralphbean/taskw/commit/1ed40ba950cc523b8ec3486bd9bf7da6fa15d4ac>`_
- Merge pull request #50 from coddingtonbear/change_tracking_and_coercion `46b277732 <https://github.com/ralphbean/taskw/commit/46b277732eb7be95c7421cf2d38ee8a78bc215d0>`_
- Test composition.  (It works..) `2de883c38 <https://github.com/ralphbean/taskw/commit/2de883c38528f53435a82ea89a2ca801fa8eae4c>`_
- Test string UDAs. `37c3c28a3 <https://github.com/ralphbean/taskw/commit/37c3c28a385558ee017fa6730bd62819aeb12724>`_
- Test UDA dates. `ba4c0eb84 <https://github.com/ralphbean/taskw/commit/ba4c0eb841415e08e393cd51060c83309971e1c5>`_
- Typofix. `0f7189282 <https://github.com/ralphbean/taskw/commit/0f718928230bdcbbf7f32babdc49a292aef01fb5>`_
- Refactors TaskRc parser to match previous version written by @ralphbean. Adds tests; fixes #51. `17f41c6e0 <https://github.com/ralphbean/taskw/commit/17f41c6e0029c0622e68200104cb6d71889f7aee>`_
- Merge pull request #52 from coddingtonbear/issue_51 `e0d6415cb <https://github.com/ralphbean/taskw/commit/e0d6415cb6b75eeaa5090fb248049a66e6768547>`_
- Merge configuration overrides into taskrc configuration. `e5b7a502d <https://github.com/ralphbean/taskw/commit/e5b7a502dc05c702a072a043e16c5adb61738f35>`_
- Update existing use of config overrides to match new datatstructure. `7278ce33e <https://github.com/ralphbean/taskw/commit/7278ce33ea84da883d7647e10c165023b5ce7a1d>`_
- Merge pull request #53 from coddingtonbear/handle_config_overrides `3c8adfe5f <https://github.com/ralphbean/taskw/commit/3c8adfe5fdf01e4a9d225faa10cf783b845a8b0b>`_
- Raise an exception if we can't parse configuration; ignore simple config values to allow storing complex ones. `fc1beaee5 <https://github.com/ralphbean/taskw/commit/fc1beaee5c20b6aa1c78b1b63571bfba5327ad05>`_
- Add AnnotationArrayField for handling idiosyncrasies of annotations. `ef3aca65f <https://github.com/ralphbean/taskw/commit/ef3aca65f9c6df642d5d2ee68e491e50df6f1846>`_
- Attempt to convert incoming string into int or float. `2726efaf0 <https://github.com/ralphbean/taskw/commit/2726efaf069edf8afb5d03b57083e218b44eda59>`_
- Only attempt to change fields known to have changed if using new journaled task. `5b7cb71b7 <https://github.com/ralphbean/taskw/commit/5b7cb71b73c7ecb8c4a89471470b365258f933e2>`_
- Handle none values. `51f003c3e <https://github.com/ralphbean/taskw/commit/51f003c3ee5f4c9fd59f78452fb9fc090e411e86>`_
- Properly handle changes to annotations. `deab4070a <https://github.com/ralphbean/taskw/commit/deab4070a833ac0919285493926f67a0ff490a4a>`_
- Allow comma-separated UUID field to properly handle null values. `aa5b6b3f9 <https://github.com/ralphbean/taskw/commit/aa5b6b3f9d9e7ac99801d13e0ca6a584165647ab>`_
- Assume that fields with registered converters are present on task record. `f81746f65 <https://github.com/ralphbean/taskw/commit/f81746f6515270ae3feaf811076066504d480f8e>`_
- Use six.text_type rather than str. `c4cc90f45 <https://github.com/ralphbean/taskw/commit/c4cc90f4529340be23ebfea9c6edb8ca984599ce>`_
- Preserve all annotation information should we have it, but still handle outgoing and incoming values as if they were strings. `e1f497291 <https://github.com/ralphbean/taskw/commit/e1f497291ac12848b4cefc89068803d1867d0702>`_
- Adding tests verifying this behavior. `02444fd75 <https://github.com/ralphbean/taskw/commit/02444fd7542fca88910d7038534abccb106f11af>`_
- Merge pull request #54 from coddingtonbear/cautious_configuration_handling `e4b02c5d3 <https://github.com/ralphbean/taskw/commit/e4b02c5d3122048892c07d6074dfdbe7bba51602>`_
- Merge pull request #58 from coddingtonbear/csuuid_field_enhancements `95eace2e5 <https://github.com/ralphbean/taskw/commit/95eace2e560d1995e8df3d1946a0973aea963e79>`_
- Merge pull request #59 from coddingtonbear/assume_specified_fields_have_value `7bf7dd5aa <https://github.com/ralphbean/taskw/commit/7bf7dd5aaf4ecb199ce311c020a15311d51fd183>`_
- Merging in upstream changes. `dfd59319a <https://github.com/ralphbean/taskw/commit/dfd59319ab5bf572712d462401423a6392f6101e>`_
- Merge pull request #57 from coddingtonbear/only_change_if_changes_exist_when_using_modern_task `78eef2a76 <https://github.com/ralphbean/taskw/commit/78eef2a76703eb1129e9b8169b6532f7e930ed7e>`_
- Merge pull request #56 from coddingtonbear/properly_deserialize_numbers `9dedffe03 <https://github.com/ralphbean/taskw/commit/9dedffe032cf0c89a3e84b6b590e80d1ac7dc989>`_
- Merge pull request #55 from coddingtonbear/annotation_field `f8511d1fd <https://github.com/ralphbean/taskw/commit/f8511d1fd1983e9a531d15e6b5beb7a7b2aca4f0>`_
- Make annotations really be strings, just special ones. `8d20fdcd4 <https://github.com/ralphbean/taskw/commit/8d20fdcd45412466f8c9393fed3c9e5293a81c0e>`_
- That's surprising, but I suppose __new__ takes care of these detais. `8d62c4750 <https://github.com/ralphbean/taskw/commit/8d62c47508520d6fdd46d90a10af553d3865b79c>`_
- Properly handle parsing choices from UDAs. `4077de023 <https://github.com/ralphbean/taskw/commit/4077de0234f717faee82d9a3c832f393143cbd1b>`_
- Do not record changes when both the former and latter values are Falsy `0f1a692c8 <https://github.com/ralphbean/taskw/commit/0f1a692c80a9bcdbf5fa9c35489d7f4196df8edb>`_
- Merge pull request #62 from coddingtonbear/fix_choices_handling_udas `c6f02f62e <https://github.com/ralphbean/taskw/commit/c6f02f62eb721215bfff706d0debdbb476640c5f>`_
- Merge pull request #63 from coddingtonbear/none_and_none_are_none `e2ef3bd9d <https://github.com/ralphbean/taskw/commit/e2ef3bd9ddf1dabe43cc4adeac0014382fc21e8c>`_
- Merge pull request #61 from coddingtonbear/better_annotation_objects `f90fcc6fe <https://github.com/ralphbean/taskw/commit/f90fcc6fe3f82b0ef04b4c694e17574545490ba6>`_

0.8.1
-----

- Expand TaskwarriorError output to include the command. `cbc2e98c1 <https://github.com/ralphbean/taskw/commit/cbc2e98c1e6d3c5907c84a48f75db75ef24a9f49>`_
- That's a list.. whoops! `22b2c6cad <https://github.com/ralphbean/taskw/commit/22b2c6cadcdb103c6609ffeb495737854571ebae>`_
- These also need to be escaped. `0b468ea6b <https://github.com/ralphbean/taskw/commit/0b468ea6bcc33c1484cd171485ebfa990b0b3d0d>`_
- Add some passing tests of task filtering. `12d1dbf32 <https://github.com/ralphbean/taskw/commit/12d1dbf3254fd7841856bf6551db6f2af6dba4fd>`_
- Test and fix a problem with filter encoding. `fa468d4a3 <https://github.com/ralphbean/taskw/commit/fa468d4a3dbbabf9df641bc12bed559fb511ce20>`_
- Test and fix another problem with filter encoding. `7900cd9e1 <https://github.com/ralphbean/taskw/commit/7900cd9e16378d7852712f3a937fd647be8dc2f0>`_
- Add some other similar tests that all pass. `982fdcf6b <https://github.com/ralphbean/taskw/commit/982fdcf6b3ace0426a2135bcfc6221132a9a4761>`_
- Test and fix another problem with filter encoding. `08950fff2 <https://github.com/ralphbean/taskw/commit/08950fff2b58e111db81290e701d74e28912d8b9>`_
- Test and implement logical operations in task filters. `3ef025c31 <https://github.com/ralphbean/taskw/commit/3ef025c3117d69d280c0e522f7fc777d56ff1bf8>`_
- Add a test for encoding of slashes. `079973a9f <https://github.com/ralphbean/taskw/commit/079973a9f699085a0b1474478b755003b6aff9af>`_
- Test and fix annotation escaping. `1a868cfdf <https://github.com/ralphbean/taskw/commit/1a868cfdf999789a6d7a5c8fd4513c2d86b7e820>`_
- subprocess is expecting bytestrings. `16e9d00e7 <https://github.com/ralphbean/taskw/commit/16e9d00e799eb0ddcbd07aeb98d76d16d10bece7>`_

0.8.0
-----

- Switch .sync to also utilize common _execute interface. `db29c60c8 <https://github.com/ralphbean/taskw/commit/db29c60c8a99f084d70dd9ed697ae88d48630378>`_
- Merge pull request #32 from latestrevision/sync_to_execute `0dd85cffd <https://github.com/ralphbean/taskw/commit/0dd85cffd765620427ad7df96e1150b73053876d>`_
- Support datetime objects as input. `48f7734b0 <https://github.com/ralphbean/taskw/commit/48f7734b080b848b1589594ca85ee560bd97f82e>`_
- Merge branch 'develop' of github.com:ralphbean/taskw into develop `f4760baf7 <https://github.com/ralphbean/taskw/commit/f4760baf76edebaecec62a9e2190e5ca9fba7359>`_
- Update the readme. `db00a1b91 <https://github.com/ralphbean/taskw/commit/db00a1b9186dc2c7fd4f76e7da54414fac9fd30f>`_
- py3 compat. `73bd7d924 <https://github.com/ralphbean/taskw/commit/73bd7d924956f8c69b04e3aabfc8d5530bbe2c6e>`_
- Of course, handle unicode as well as byte strings here... `ef09c4073 <https://github.com/ralphbean/taskw/commit/ef09c4073f00adc9533493a5068c5a7499ba8f85>`_
- Test that unicode stuff. `9b394d513 <https://github.com/ralphbean/taskw/commit/9b394d513cd652af09492d90abcd5f819f0c1615>`_
- Serialize incoming zoned date/datetime instances into strings of the appropriate format before relaying to taskwarrior. `0516cc10c <https://github.com/ralphbean/taskw/commit/0516cc10c229e4e0625c5a8ed3e1e145ff153fe4>`_
- Adding two additional requirements (sorry). `2f3264d2b <https://github.com/ralphbean/taskw/commit/2f3264d2ba1d621282f90b98fe73258b95526f61>`_
- Fixing requirement name. `850b75c7b <https://github.com/ralphbean/taskw/commit/850b75c7b81ca3522dcda3dfa4bb180972be0b6a>`_
- Minor modifications to annotation handling to support annotations in 2.3.0 `c2f1e4fae <https://github.com/ralphbean/taskw/commit/c2f1e4faecec7e6c77a4529556a5a6cba519a67a>`_
- Overriding _stub_task to preserve due date; display the actual error message when a task is not creatable. `290a93f34 <https://github.com/ralphbean/taskw/commit/290a93f34bfa2a7f693b9ab1c5ac36c4908b925c>`_
- Use string_types rather than basestring. `a33aa47a9 <https://github.com/ralphbean/taskw/commit/a33aa47a918ba59eec3ce08fb91a5aeaf3d5fee4>`_
- Removing unicode literal. `037b22622 <https://github.com/ralphbean/taskw/commit/037b2262288975427c5f4382108a3766f79b0abc>`_
- Use six.text_type rather than a unicode literal. `40ef622ea <https://github.com/ralphbean/taskw/commit/40ef622ea835a25c1aa22b7b2a7b95a35646f9f6>`_
- Use string_types rather than basestring. `546a9de89 <https://github.com/ralphbean/taskw/commit/546a9de89fb79a6c985ff665427cf077bf8182cf>`_
- Use six.text_type rather than a unicode literal. `e94459981 <https://github.com/ralphbean/taskw/commit/e94459981912bd21486f69f9a59c963616b5fc56>`_
- Do not attempt to set parameters unless they are explicitly defined in the incoming data. `30750abee <https://github.com/ralphbean/taskw/commit/30750abee14803f1075c32ca66ab220e686c904a>`_
- Gracefully handle situations in which id or uuid is unspecified. `790b7b044 <https://github.com/ralphbean/taskw/commit/790b7b044154f784788da0c16a0b1b92ea34b248>`_
- Merge pull request #34 from latestrevision/fix_date_serialization `c0f7a1f76 <https://github.com/ralphbean/taskw/commit/c0f7a1f76372274d26781b6ab7bdaf115914d0bb>`_
- Merge branch 'fix_annotation_handling' into develop `f313d2800 <https://github.com/ralphbean/taskw/commit/f313d28005b853b23c12885c6e7a48a9c2ec90bd>`_
- Avoid hardcoding TZ in the test expectation. `d696409bd <https://github.com/ralphbean/taskw/commit/d696409bd3f6c410a860cb2570215a4c8b54e046>`_
- Add functionality for marking existing task as started/stopped. `b7926d2ec <https://github.com/ralphbean/taskw/commit/b7926d2ecb8d8c9a3b987b90a9a901fa83d3c1d1>`_
- Return stdout or stderr from task_info. `c83b5ac81 <https://github.com/ralphbean/taskw/commit/c83b5ac8179127f22081e4babd23be6ced77f9e3>`_
- Merge pull request #36 from latestrevision/add_start_and_stop `860bf5176 <https://github.com/ralphbean/taskw/commit/860bf5176e2781a19eb4486b55944a3fc49b0cf4>`_
- Merge pull request #37 from latestrevision/fix_info_method `5e46a51ac <https://github.com/ralphbean/taskw/commit/5e46a51accbc6ef0e1e69f0037cce882b6b6ab0d>`_
- Removing duplicated encoding of string types. `0dccea5ca <https://github.com/ralphbean/taskw/commit/0dccea5ca92fc6f956321c000a538d0a6f4900ac>`_
- Merge pull request #38 from latestrevision/remove_duplicated_encoding_for_string_items `9031179c8 <https://github.com/ralphbean/taskw/commit/9031179c8ce0f6fb47ff7fca3b5e4e00339ad497>`_
- Convert 'None' into an empty string; otherwise, we will ask task to set various fields to the string value None. `14eb7c4ae <https://github.com/ralphbean/taskw/commit/14eb7c4aec2d1c90ff679e53751362dce9a488c5>`_
- Merge pull request #39 from latestrevision/properly_empty_values_upon_null `5eb1fdbec <https://github.com/ralphbean/taskw/commit/5eb1fdbec33192827c0a1012132ea302403fa0fc>`_
- Raise an exception when taskwarrior has a non-zero return status. `8bb389997 <https://github.com/ralphbean/taskw/commit/8bb389997d5d8a3ed4b82a3e42b95ea6eb216ded>`_
- Merge pull request #40 from latestrevision/raise_on_error `1a5c0d468 <https://github.com/ralphbean/taskw/commit/1a5c0d468706049a5ee3bb4fe74393387ab1faa5>`_
- Manually assign UUID of task before creation to ensure that retrieval is successful. `782e9f6f0 <https://github.com/ralphbean/taskw/commit/782e9f6f0e9f7122fd6b53b234276a8bd7b81113>`_
- Merge pull request #41 from coddingtonbear/manually_assign_uuid_to_added_tasks `d1afcbd48 <https://github.com/ralphbean/taskw/commit/d1afcbd486951822aad81cf78a0f361e26f637ef>`_
- Alter TaskWarriorShellout such that one can easily define new config overrides in subclasses. `2c3344d3a <https://github.com/ralphbean/taskw/commit/2c3344d3a532a0d1903e34760cfd220fea7a71ce>`_
- Use a slightly more untuitive data structure for storing config overrides. `a1c7fde67 <https://github.com/ralphbean/taskw/commit/a1c7fde67e0d3e3496dd0fd816c3709d37cc0c0a>`_
- Removing unncessary unicode string marker. `5ce28c699 <https://github.com/ralphbean/taskw/commit/5ce28c6991218b7bb75d6ea62ed560918f3fc448>`_
- Merge pull request #42 from coddingtonbear/allow_subclass_configuration_overrides `ebaa6967f <https://github.com/ralphbean/taskw/commit/ebaa6967fbad97d5654905f43eb82330dc397b60>`_
- Do not test deletion of completed tasks with Shellout; this operation is not supported by taskwarrior. `5ca1d61e1 <https://github.com/ralphbean/taskw/commit/5ca1d61e1116bb7545e619a804e392021dd0762d>`_
- Merge pull request #43 from coddingtonbear/fix_test_delete_completed `203c38694 <https://github.com/ralphbean/taskw/commit/203c386942d06000a50e20eea36907dd6e5220a5>`_
- Adding 'filter_tasks' method accepting a dictionary of filter arguments for returning from taskwarrior. `99fc349fc <https://github.com/ralphbean/taskw/commit/99fc349fcc29c8ed28f3f191b51048b65f863880>`_
- Adding a docstring. `b5d897607 <https://github.com/ralphbean/taskw/commit/b5d897607ecbf06a6dcda12b8454fa4a702f7889>`_
- Merge pull request #44 from coddingtonbear/add_filter_tasks_method `2514cd584 <https://github.com/ralphbean/taskw/commit/2514cd584d735417f58edd0fc1222527de378513>`_
- Distinguish between escaping a query and escaping on issue creation. `333e26919 <https://github.com/ralphbean/taskw/commit/333e26919942efc8282eba3473cb0b17825483e5>`_
- Merge pull request #45 from coddingtonbear/distinguish_query `f98ed1620 <https://github.com/ralphbean/taskw/commit/f98ed162010487ec4d41f3b096d2ef54961d021d>`_
- Minor fixes relating to UDA handling; improving exception message. `253aad5d9 <https://github.com/ralphbean/taskw/commit/253aad5d92333e5034c4a1ef3381b014bec77fd1>`_
- Better annotation handling. `209050dab <https://github.com/ralphbean/taskw/commit/209050dabd9e78feb1380751144c266368f6520a>`_
- Allow passing "init" arg to sync command `3b9ae8e68 <https://github.com/ralphbean/taskw/commit/3b9ae8e68bc40fd6e5503a8da4670ee29327e507>`_
- Merge pull request #48 from kostajh/sync-init `a1da55d30 <https://github.com/ralphbean/taskw/commit/a1da55d309e2cb6d3b720e3667744a31b414b875>`_
- Merge pull request #47 from coddingtonbear/minor_fixes_supporting_bugwarrior `e1332c2a1 <https://github.com/ralphbean/taskw/commit/e1332c2a14c7ce0dd40a7b99f7f3263c45eb29a5>`_
- Don't hardcode ascii. `459ab8911 <https://github.com/ralphbean/taskw/commit/459ab891155481ff0ee935b2ba7785ec912cdc94>`_

0.7.2
-----

- Add some failing test cases based on a report from @lmacken. `807eebdfc <https://github.com/ralphbean/taskw/commit/807eebdfca9c8475e3399c56240e0995c3492630>`_
- This should fix it. `ad5ad2f70 <https://github.com/ralphbean/taskw/commit/ad5ad2f708db26f96999c6b6ed5a71f767d9379f>`_
- Merge branch 'feature/backslashes-omg' into develop `8b44795d9 <https://github.com/ralphbean/taskw/commit/8b44795d942d1d7477ab69a27f50a017393491be>`_

0.7.1
-----

- Add back forgotten import. `6e3bf593e <https://github.com/ralphbean/taskw/commit/6e3bf593ee253cbefb10900aaee41daed8f1e17f>`_

0.7.0
-----

- Allow passing tags as part of the task `60ca9d39f <https://github.com/ralphbean/taskw/commit/60ca9d39f449c5db1b180e13857e9d067a1f5440>`_
- Adding 'sync' capability; cleaning-up version checking. `1acb2cb9e <https://github.com/ralphbean/taskw/commit/1acb2cb9e2c99ca54ee0b335e225ff221a8e8ab7>`_
- Make taskwarrior version gathering support taskwarrior residing at a non-standard path. `6359d79e3 <https://github.com/ralphbean/taskw/commit/6359d79e35c75af404f27a778ca2b9d9f13baaee>`_
- Adding TaskWarrior.sync (raises NotImplementedError). `a628990bf <https://github.com/ralphbean/taskw/commit/a628990bf96ce516bbb28c5f657cc122f12e1e4e>`_
- Merge pull request #28 from latestrevision/add_sync_capability `647f3378e <https://github.com/ralphbean/taskw/commit/647f3378e484c58ff81749f6036d75f91463a106>`_
- Refactor such that all commands share a single interface. `9cb4edf11 <https://github.com/ralphbean/taskw/commit/9cb4edf118fe1e264657c75e10ff7eb0472f409b>`_
- Merge pull request #24 from kostajh/develop `b5f90f73b <https://github.com/ralphbean/taskw/commit/b5f90f73b969a0caff62b56cc074d9105745811d>`_
- Replacing string literal with variable. `25fedee85 <https://github.com/ralphbean/taskw/commit/25fedee850b0f9cd56e2bada7926a2e488387e8a>`_
- Removing unicode literal. `344a354ea <https://github.com/ralphbean/taskw/commit/344a354eae4d9574df357a44474edcb490a408ee>`_
- Decode incoming strings using default encoding before deserialization. `d5a1b5ab7 <https://github.com/ralphbean/taskw/commit/d5a1b5ab794cb5e362bb9523d0f345a15d91fd6e>`_
- There is no reason for me to have written such a complicated sentence. `84bc5f9b7 <https://github.com/ralphbean/taskw/commit/84bc5f9b70b55b7e24ae7af05502d232079f3882>`_
- Merge pull request #29 from latestrevision/rearchitect_twe `9b43c38e4 <https://github.com/ralphbean/taskw/commit/9b43c38e4ea3bf7fd985b71fe02e72709991b010>`_
- Make TaskWarriorShellout our default. `df9be4a41 <https://github.com/ralphbean/taskw/commit/df9be4a410d4e0a7b22d122445a37c30644e33d4>`_
- PEP8. `c222da89e <https://github.com/ralphbean/taskw/commit/c222da89e4cbf4c6e32866fe476c433de5f33e2d>`_
- Merge branch 'develop' of github.com:ralphbean/taskw into feature/switchover `f2a3c0b28 <https://github.com/ralphbean/taskw/commit/f2a3c0b2824cc5770c09ccb65bbcc551557aebab>`_
- Provide a backwards compatibility rename. `2a548993f <https://github.com/ralphbean/taskw/commit/2a548993fbfa21810abe6189eac9d4f0d4ec4bb4>`_
- Add a lot more tests to the shellout implementation. `f1c4e7706 <https://github.com/ralphbean/taskw/commit/f1c4e770650faa50a98aaa000e994a16b6cabfb6>`_
- Standardize the load_tasks method. `143b69a0a <https://github.com/ralphbean/taskw/commit/143b69a0a022bf20b46b436f44cfdba8b3a896dd>`_
- You cannot fake annotations like this with the shellout approach. `2e4d674ac <https://github.com/ralphbean/taskw/commit/2e4d674ac888a876e2e7e34cf6fe9a09cdf13a34>`_
- These tests no longer make sense. `a9b53d911 <https://github.com/ralphbean/taskw/commit/a9b53d911a954ab506585e75c034fd96585f2451>`_
- We never had a task_delete method for shellout.  Here it is. `d9ddd9c79 <https://github.com/ralphbean/taskw/commit/d9ddd9c79903902fa1b0a436b445cf6b1e7e4387>`_
- deletes, though, require confirmation.... `5c01dab4c <https://github.com/ralphbean/taskw/commit/5c01dab4c60a0c8b3b857a80b00b86d5bbf3523e>`_
- Cosmetic. `9240706e4 <https://github.com/ralphbean/taskw/commit/9240706e43141c4f6ac2beb4e20daec0cbaebed7>`_
- Make this return signature standard. `1a868b9b3 <https://github.com/ralphbean/taskw/commit/1a868b9b39603450a70e6fc596c035e02a802f9d>`_
- Allow user to specify the encoding. `ddf4df91a <https://github.com/ralphbean/taskw/commit/ddf4df91ab830b8b33dcc0cd883c25f0a4c557f5>`_
- Merge the "waiting" list back into the "pending" list. `3d9f050f9 <https://github.com/ralphbean/taskw/commit/3d9f050f9825ff2d423efc6ef0b480d68c20d7c6>`_
- Really merge.. not overwrite. `a4bfb5e88 <https://github.com/ralphbean/taskw/commit/a4bfb5e8872c4dca5c3a23d946554069e6d9f75a>`_
- Add TaskWarriorExperimental back to __all__ `ac7b227c2 <https://github.com/ralphbean/taskw/commit/ac7b227c2a3b607d07d0c564502716324cc5cf61>`_
- We actually do install 'task' in our travis environment. `7518d0aeb <https://github.com/ralphbean/taskw/commit/7518d0aeb3634700897c99550ce9be1d5e5a86a5>`_
- Merge pull request #31 from ralphbean/feature/switchover `d63bb0f43 <https://github.com/ralphbean/taskw/commit/d63bb0f43d8889cbc2485c33e743953ff0144745>`_

0.6.1
-----

- Install taskwarrior for Travis CI tests `a59d8dd0f <https://github.com/ralphbean/taskw/commit/a59d8dd0f708cbcf314eb513dfc7f2288ddb982a>`_
- Add complete example for experimental mode `2210ae394 <https://github.com/ralphbean/taskw/commit/2210ae39410bbd64d2ac68f1ad6c2f96c1323ce1>`_
- Check what version of task we have installed `fc6a03c80 <https://github.com/ralphbean/taskw/commit/fc6a03c80d13a7f260e82ca390e3c436d10a764a>`_
- Try installing 2.2 version of TW `f3e5a9971 <https://github.com/ralphbean/taskw/commit/f3e5a9971dda83c17c84d642fc6c737fefc215e1>`_
- Yes, we want to add the repo `baeec9de0 <https://github.com/ralphbean/taskw/commit/baeec9de0781850fa8fb745d48ceea10bb313b45>`_
- Just check for TW version 2. `cf6f3d881 <https://github.com/ralphbean/taskw/commit/cf6f3d881e51e9c14466ab9cb1eed5a98d2e71f8>`_
- Update tests, make an important fix in _load_task for handling single vs multiple results `98fe47538 <https://github.com/ralphbean/taskw/commit/98fe47538909c4d516aef68b16991726406fa9fb>`_
- Fix tests for TWExperimental, all tests pass now in Python 2.7 `ba91fdeab <https://github.com/ralphbean/taskw/commit/ba91fdeab7d39873645279facf865e9f2b6db979>`_
- basestring should be replaced with str for python 3 `3cdbb74a0 <https://github.com/ralphbean/taskw/commit/3cdbb74a08cf38f4ca285c6d721215cc910024fe>`_
- More python3 compatibility `e6018e5dc <https://github.com/ralphbean/taskw/commit/e6018e5dc84704eeeb1df40b314e185d5c30de89>`_
- Fix encoding of subprocess results `a79b4ffd0 <https://github.com/ralphbean/taskw/commit/a79b4ffd02642c179fdaf64f0ead39360e17e659>`_
- Fix encoding for another subprocess call `1a10e302b <https://github.com/ralphbean/taskw/commit/1a10e302bdde50d31d61a0742039570e1308e9e1>`_
- add task deannoate function to Experiemental `17e5ce813 <https://github.com/ralphbean/taskw/commit/17e5ce813426bac6effca039f3d993e882bc04ff>`_
- Fix decode issues with subprocess results for python 3 `f2b886ccd <https://github.com/ralphbean/taskw/commit/f2b886ccdbf3d8cd7097d4088c0eef91aaff76ab>`_
- Merge pull request #22 from kostajh/develop `13d3c7b93 <https://github.com/ralphbean/taskw/commit/13d3c7b93f9ad5c561390937a101219ea243dfce>`_
- Merge pull request #23 from tychoish/develop `853ba71b2 <https://github.com/ralphbean/taskw/commit/853ba71b22d69163934cf0ca2dd1b1567da7f23b>`_
- Split only once. `ba00547ab <https://github.com/ralphbean/taskw/commit/ba00547aba52a0684f765190537434edc48e70d6>`_
- Get the key only if it exists. `a9da7ee29 <https://github.com/ralphbean/taskw/commit/a9da7ee298336995e3c28758ce806394878417d6>`_
- Set a default data location if one is not specified. `0cb7ef36f <https://github.com/ralphbean/taskw/commit/0cb7ef36fbdc7b9009cfee8c1c5c98435dcace74>`_
- Try a test for #26. `e10bd5516 <https://github.com/ralphbean/taskw/commit/e10bd55163473529895786ef9cbe264e078c8906>`_

0.6.0
-----

- Import six `6b4774237 <https://github.com/ralphbean/taskw/commit/6b477423735e1f46d1a6629fee5028292dc2b9ce>`_
- Merge pull request #16 from kostajh/develop `ae0c90e3d <https://github.com/ralphbean/taskw/commit/ae0c90e3d7c624d40a6f844221afa718cc0b9c66>`_
- PEP8. `40803afae <https://github.com/ralphbean/taskw/commit/40803afaeaec89f1ae865eab35f178e66e49f180>`_
- Run tests on both normal and experimental implementations. `4305eb0c5 <https://github.com/ralphbean/taskw/commit/4305eb0c5170b4a32ec6031a0c183faa2902084c>`_
- Note support for py3.3 `bfd0e9dd6 <https://github.com/ralphbean/taskw/commit/bfd0e9dd6ed532487ec3c6d2714fc61fcdfaacff>`_
- PEP8. `d09539ad1 <https://github.com/ralphbean/taskw/commit/d09539ad1c3e164b345e0840ef0ea0eb7e6f5912>`_
- Try to support skiptest on py2.6. `0b691cd09 <https://github.com/ralphbean/taskw/commit/0b691cd0944808c22b890ce30385169169ebabb6>`_
- Spare them the spam. `462f8e138 <https://github.com/ralphbean/taskw/commit/462f8e1383ed84eb0b402765367cc2d40dc7d8f8>`_
- Added forgotten import. `ba2806e29 <https://github.com/ralphbean/taskw/commit/ba2806e291d3ceb66c50d06edf33dcb7f1ad1ce0>`_
- Oh.  This is a lot easier. `08c9e0f07 <https://github.com/ralphbean/taskw/commit/08c9e0f07f2524fd362626c22e000ffb20d8cbcd>`_
- Compatibility between experimental and normal modes. `cc4a4c339 <https://github.com/ralphbean/taskw/commit/cc4a4c339a125f0df415cefdedbeb27730102f54>`_
- Delete modified field from task `8419c6617 <https://github.com/ralphbean/taskw/commit/8419c661783c836b0f1884b7eb63cde092cdf22d>`_
- Merge pull request #17 from kostajh/develop `ee07d8957 <https://github.com/ralphbean/taskw/commit/ee07d8957ff73e4cde941d865ea57f3bfb097f57>`_
- Do not replace slashes when in experimental mode `19b52a3ae <https://github.com/ralphbean/taskw/commit/19b52a3ae634c61f6e1a311dd6685a3d9b80dedb>`_
- Merge pull request #18 from kostajh/develop `f5c77fdd1 <https://github.com/ralphbean/taskw/commit/f5c77fdd151d4f3de873eb37f97a578c72e589ec>`_
- Be more gentle with the timestamp test. `853a1693e <https://github.com/ralphbean/taskw/commit/853a1693e9f5a6b78c6e5938e32cceeab353f4da>`_
- Add failing test against experimental mode. `a12738dbd <https://github.com/ralphbean/taskw/commit/a12738dbd87da635d09d117d8071d94f04b44e80>`_
- Merge branch 'develop' of github.com:ralphbean/taskw into develop `81330d741 <https://github.com/ralphbean/taskw/commit/81330d741b708a9f66c46d259c2d1ff84c84f44b>`_
- Skip experimental tests of taskwarrior version is too low. `59cdb5a33 <https://github.com/ralphbean/taskw/commit/59cdb5a3330b230edc848930b973043f1c007c8d>`_
- Check if we have a string before calling replace(). `d43dc2002 <https://github.com/ralphbean/taskw/commit/d43dc200287478746d67caa1c8d026e0bf6dcd6f>`_
- Allow non-pending tasks to be modified. `6a1326816 <https://github.com/ralphbean/taskw/commit/6a1326816169c4340d2dba4b4b4b4a6127be6ccb>`_
- Merge pull request #19 from kostajh/develop `7c72ddf0f <https://github.com/ralphbean/taskw/commit/7c72ddf0f4d9098a9da4f0ddee00ba1985f4bc85>`_
- Py3 support. `6bd5b1cca <https://github.com/ralphbean/taskw/commit/6bd5b1cca3ff0234bb7d82d0151ba3bd7cce82a7>`_
- Merge pull request #14 from burnison/completed_task_inclusion `ddb9bab62 <https://github.com/ralphbean/taskw/commit/ddb9bab62e8260d79b9e0c310bdf9cd4f85cb73a>`_
- Refactor _load_tasks(). Fixes #20 `595475b9d <https://github.com/ralphbean/taskw/commit/595475b9d41fb49fa0b42a8164226736d6b10420>`_
- Check if 'status is in task. `e521acc96 <https://github.com/ralphbean/taskw/commit/e521acc961871e7d52922cb4ff6d8dec9a40d137>`_
- Don't assume that we always find a task. `0af6d038d <https://github.com/ralphbean/taskw/commit/0af6d038db8a860889ee8c2f9780939c5002603c>`_
- If task does not have uuid, don't proceed with update `259218f18 <https://github.com/ralphbean/taskw/commit/259218f18ad44160f356319d6302a8f0f496b72f>`_
- Allow for using keys being id, uuid and description (for example, search by UDA) `6be8c8a65 <https://github.com/ralphbean/taskw/commit/6be8c8a65425105906092733fc7eb14d55626928>`_
- Minor fix to previous commit `d8d6a96d0 <https://github.com/ralphbean/taskw/commit/d8d6a96d073902e3e4d1b2c110be2814d8e5ffac>`_
- Do not require confirmation when updating task `88338365e <https://github.com/ralphbean/taskw/commit/88338365e9f18201767146ec49233e4412cd2c2f>`_
- Fix the logic for checking what kind of key we have. `6c4c55e78 <https://github.com/ralphbean/taskw/commit/6c4c55e78e8b072c29b10ed280fa042dbd7a36d2>`_
- Fix _load_task for ID and UUID `e204e93b2 <https://github.com/ralphbean/taskw/commit/e204e93b270872a93a9778accec0a0a810f01873>`_
- Raise an alert if there is no uuid in task_update `840dfcef3 <https://github.com/ralphbean/taskw/commit/840dfcef3754557b19b05b9ee4b13adf06d22396>`_
- Strip whitespace from task description `5b1b57fd6 <https://github.com/ralphbean/taskw/commit/5b1b57fd6f5ae622a7ef0bc97e4a9b689920d194>`_
- Python3 compatibility `d46ec7f08 <https://github.com/ralphbean/taskw/commit/d46ec7f084dea302965ec339fab877773d3049fb>`_
- Merge pull request #21 from kostajh/load-task-refactor `98b1c4481 <https://github.com/ralphbean/taskw/commit/98b1c4481541b8fb2dd5a32dbc9e7ecc0b0a966a>`_
- Py3.2 fix. `c091e27bb <https://github.com/ralphbean/taskw/commit/c091e27bb7019afc4219b7aedcfe9eec7b9f5b02>`_

0.5.1
-----

- Missing import. `f9b2bd450 <https://github.com/ralphbean/taskw/commit/f9b2bd4509613c8321358462ea92ce70c8b5b3d3>`_

0.5.0
-----

- Add ability to specify 'end' time on task closure. `e926560fc <https://github.com/ralphbean/taskw/commit/e926560fcb1b6103862de0441983283efc62ec76>`_
- Remove set literal for python 2.6 compatibility. `122d33477 <https://github.com/ralphbean/taskw/commit/122d334779fe67f171075cd0bb4af5d3ed69a3b9>`_
- Merge pull request #13 from burnison/end_date_on_closure `1eeadbe4a <https://github.com/ralphbean/taskw/commit/1eeadbe4a6b829f8d09b118ee3165b5ad8c08de9>`_
- Allow loading tasks using task export `4f5f116ac <https://github.com/ralphbean/taskw/commit/4f5f116acad9107987451fc6b36f48c5f923b20f>`_
- Adjust encode task to our needs. `8a9a9ddb9 <https://github.com/ralphbean/taskw/commit/8a9a9ddb990e28fb723e03fb50c09051f24a15da>`_
- Add support for task add and task done. `030f60976 <https://github.com/ralphbean/taskw/commit/030f609767bf60921ef41f2193b1fc267e1bd1da>`_
- Add task modify support `7a96b33ed <https://github.com/ralphbean/taskw/commit/7a96b33ed59b32a5a7c35e3ac3c0475391f362d2>`_
- Make subprocess calls quiet `72fb0a4a9 <https://github.com/ralphbean/taskw/commit/72fb0a4a909cdde54f3ba3699d06bcc111dfb2a0>`_
- We do not need pprint `19ec0c106 <https://github.com/ralphbean/taskw/commit/19ec0c10615d44fa711034694adb2e23d91153eb>`_
- Add task_annotate method `09da090ab <https://github.com/ralphbean/taskw/commit/09da090ab5f5a824c6eb72ed67386af992663581>`_
- Add TODO for checking annotations `00c83a52a <https://github.com/ralphbean/taskw/commit/00c83a52a1e1aa18b9436522479f66d0ee78adce>`_
- Extract annotations passed into task_add `b9a4367cd <https://github.com/ralphbean/taskw/commit/b9a4367cd6cd149da6ba886310f3d821f23f32e5>`_
- Add support for updating annotations `825b3d324 <https://github.com/ralphbean/taskw/commit/825b3d324b25c038a4052a82737a84432b475107>`_
- Make sure the config_filename is used for working with TW `23cd99777 <https://github.com/ralphbean/taskw/commit/23cd997779bd7a2f66f0bdfad1ffd22650d8a413>`_
- Add task info command `8fe9ed863 <https://github.com/ralphbean/taskw/commit/8fe9ed863252d8ca02f51b5fb4300432c69bb1e9>`_
- get_tasks can return pending or completed items `2271b0ee9 <https://github.com/ralphbean/taskw/commit/2271b0ee9239748962b5e38c0867317a706d8074>`_
- Return first match found in completed or pending tasks `9511ebfb0 <https://github.com/ralphbean/taskw/commit/9511ebfb0a697528432c35b21f4e00e65ad39c8b>`_
- Reorganize @kostajh's original and experimental approaches into subclasses of an abstract base class. `93fc7cb9c <https://github.com/ralphbean/taskw/commit/93fc7cb9c88f81584b907b57d8b2cc616b801d51>`_
- Some docstrings. `79d9b512b <https://github.com/ralphbean/taskw/commit/79d9b512bb02a97d4919c50546385ec48f9c5b8b>`_
- Turn load_config into a classmethod. `642df53bb <https://github.com/ralphbean/taskw/commit/642df53bb52ab2872610920874a87a38d5d7b2d7>`_
- Py3.2 support. `410f8bb15 <https://github.com/ralphbean/taskw/commit/410f8bb1529fc4183ef8fdf78309c4f40bd30b1c>`_
- Add py3.3 to the travis tests. `12cccd044 <https://github.com/ralphbean/taskw/commit/12cccd0447d0c35795b0134aee8523b30490c81f>`_
- Update the README; preparing for release. `8b3758702 <https://github.com/ralphbean/taskw/commit/8b3758702ae3a8985193002f3d2846449566b7ac>`_

0.4.5
-----

- Add support for due dates using UNIX timestamps `683f14e81 <https://github.com/ralphbean/taskw/commit/683f14e81c266c4780ddf1558d3ca530b5c98f66>`_
- Add due timestamp for tests. Fixes #11 `10cdf73b4 <https://github.com/ralphbean/taskw/commit/10cdf73b4049bcde026512a68709f1b507e74629>`_
- Merge pull request #12 from kostajh/due-dates `dc67868b9 <https://github.com/ralphbean/taskw/commit/dc67868b9682ba89b195f848a95c1d7640309ae6>`_

Changelog
=========

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

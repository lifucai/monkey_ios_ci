# monkey_ios_ci
一、当前android打包发布流程

当前全量发布方式存在问题：
1、如果版本改动大或者风险大，如果有问题影响用户量大
2、渠道包发布后撤包流程复杂

二、android客户端灰度方案（基于用户灰度）


相关说明：
1、灰度用户来源：
已经和刘硕沟通，可以提供日活用户（可以区分用户使用设备），从多天连续活跃的用户中随机筛选1000个用户指定升级用户，之后按照用户升级比例，可以调整指定用户基数

2、灰度观测周期
预计灰度观测周期为2天，最小用户量为500

3、按照用户升级已在运营后台测试过，可以支持按照用户升级

4、灰度包，放到研发助手中

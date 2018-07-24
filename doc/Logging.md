
## V9 ELK Logging Solution ##

ELK logging solution is a populer, open source and active community logging solution which have rich functional plugin like X-Pack, so, we using ELK as the V9 sample logging solution. There is other commercial logging solution like Graylog.

Hint, all the description below base on the sample configuration file(Entrypoint.sh, filebeat.yml, dockerfile etc).

The overall design as below chart, for each Commerce container there will be a 'side car' filebeat container help to collect the log in real time, by leveraging the Pod shared volume ability filebeat can access Commerce log in the shared volumn directly, then beat the log to the ElasticSearch system(json format), after that you can view the log in Kibana GUI<br/>
<img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/WC_K8S_ELK.png" width = "800" height = "450" align=center />

After Kubenetes launched all the container, then you can check the log in the Kinaba by open http://<Kibana_Host>:5601.<br/>
  <img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/Kibana.png" width = "800" height = "450" align=center /><br/>

  For each line of the Commerce log there will be a corresponding entry in the Kibana, you can find it in the message field.<br/>
<img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/KibanaMessageField.png" width = "600" height = "335" align=center /><br/>
  <what we customize>

## Why we need to build customized filebeat docker image and how ##

In order to simplify the deployment work in Kubernetes, in the sample we put the customized filebeat configuration file filebeat.yml and the docker initlization file Entrypoint.sh inside the customized filebeat docker image. In this way, build the customized image once, it can apply for different Commerce container compoent like Search, Foundation etc by point to different filebeat.yml in the Entrypoint.sh.


Pull the filebeat docker image from the official repository(better to have a local repository to accelerate the pull speed), modify the sample dockerfile, Entryponit.sh and Filebeat.yml base on your needs, then build the customized filebeat image. <br/>
<pre>
docker build -f &lt;sample_dockerfile&gt; -t &lt;repository&gt;:&lt;tag&gt; .
</pre>
<img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/Build_Filebeat_Image.png" width = "600" height = "135" align=center /><br/>

  ### How to customize the filebeat.yml ###
  
  How to get rid of the exception stack split into multiple message in the ElasticSearch
  <pre>
  multiline.pattern: '^\['
  multiline.negate: true
  multiline.match: after
  </pre>
  
  How to add a new field help to identify&filter log by container type
  <pre>
    fields:
      containerType: search
  </pre>
  <img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/ContainerType.png" width = "300" height = "200" align=center /><br/>
  
  More information about the filebeat.yml configuration please refer to:<br/>
  https://www.elastic.co/guide/en/beats/filebeat/current/configuring-howto-filebeat.html
  
  ### How to customize the Entrypoint.sh ###

  In the Entrypoint.sh, will get the input ‘-indexName' '-targetELK' parameters from Kubernetes, update all the filebeat.yml configuration file accordingly, then, using the container specfic(search, tx etc) filebeat.yml to launch the filebeat service.<br/>
  For more details, please refer to the script Entrypoint.sh.<br/>

  ### How to customize the dockerfile ###
  
  Please refer to Docker official guide:<br/>
  https://docs.docker.com/engine/reference/builder/#usage

## Deployment Process ##

### Prerequest ###

Setting up the ElasticSearch + Kibana
  1) install the ElasticSearch (or ElasticSearch cluster) following the offical installation guide. Base on the business requirment, please consider using ElasticSearch cluster if the logging throughput is huge.<br/>
  https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html<br/>
  https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html

  2) install the Kibana following the offical installation guide.<br/>
  https://www.elastic.co/guide/en/kibana/current/install.html

 ### How to launch filebeat container alone with WC container ###
 
 Below chart is the snapshot of the sample deployment Jenkins job<br/><br/>
 <img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/Enable_Filebat&ELK.png" width = "450" height = "400" align=center /><br/>

<B>FileBeat.Enable</B>, change this flag to 'true' to enable filebeat container alone with commerce container.
<B>FileBeat.ELKServer</B>, change this to the your ElasticSearch server(or the the Master node of your ElasticSearch cluster)


  ### What is the OOB behavior of the sample ###
  
  <img src="https://github.com/IBM/wc-devops-utilities/raw/draftdoc/doc/images/Enable_Logging_logic.png" width = "500" height = "250" align=center /><br/>
  
  Using the flag 'FileBeat.Enable' in the Jenkins HelmChart_values field to contral enable the filebeat container alone with commerce container or not.<br/>


You can launch filebeat container alone with commerce container using the build-in filebeat.yml(build-in in the customized filebeat image) or using a customized filebeat.yml. If there is a customized filebeat.yml file specfied, Kubernets will using the customized one(ingore the build-in one), if customized filebeat.yml doesn't specifed, then using the build-in one.

You can specify the customized filebeat.yml by create Kubernetes configmaps. For example, define a specific filebeat configuration file for store container.<br/>
1) Define the customized filebeat configuration file(filebeat-cus.yml)
2) Create a configmap based on the customized filebeat configuration file
  <pre>
  kubectl create configmap filebeat-config-crs-app --from-file filebeat-cus.yml
  </pre>
3) Update the configmap in the values.yaml, Set the Value 'Values.Crsapp.FileBeatConfigMap=filebeat-config-crs-app'
4) The configmap will mount to the /etc/filebeat/ folder of filebeat container. The container will start with the configuration file /etc/filebeat/filebeat-cus.yml 



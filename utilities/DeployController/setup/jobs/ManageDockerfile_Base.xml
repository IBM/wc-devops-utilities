<?xml version='1.0' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@2.13">
  <actions>
    <org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@1.1.8">
      <jobProperties/>
      <triggers/>
      <parameters/>
    </org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
  </actions>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>Tenant</name>
          <description>Tenant Name</description>
          <defaultValue>demo</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>EnvName</name>
          <description>environment name</description>
          <defaultValue>qa</defaultValue>
        </hudson.model.StringParameterDefinition>
        <hudson.model.ChoiceParameterDefinition>
          <name>Component</name>
          <description>target bundle component</description>
          <choices class="java.util.Arrays$ArrayList">
            <a class="string-array">
              <string></string>
              <string>ts-app</string>
              <string>crs-app</string>
              <string>search-app</string>
              <string>xc-app</string>
            </a>
          </choices>
        </hudson.model.ChoiceParameterDefinition>
        <hudson.model.StringParameterDefinition>
          <name>NameSpace</name>
          <description>namespace name</description>
          <defaultValue>default</defaultValue>
        </hudson.model.StringParameterDefinition>
        <org.biouno.unochoice.DynamicReferenceParameter plugin="uno-choice@1.5.3">
          <name>Dockerfile</name>
          <description>Dockerfile which stored as ConfigMap for particular environment</description>
          <randomName>choice-parameter-5533183353447394</randomName>
          <visibleItemCount>1</visibleItemCount>
          <script class="org.biouno.unochoice.model.GroovyScript">
            <secureScript plugin="script-security@1.29.1">
              <script>if(Component == &apos;&apos;){
    dockerConfigMapName=&quot;dockerfile&quot;
}else{
    dockerConfigMapName=Component+&quot;-dockerfile&quot;
}
def process = [&quot;python&quot;,&quot;/commerce-devops-utilities/scripts/kube/kubcli.py&quot;,&quot;fetchconfmap&quot;,&quot;-tenant&quot;,Tenant,&quot;-env&quot;,EnvName,&quot;-name&quot;,dockerConfigMapName,&quot;-namespace&quot;,NameSpace].execute()
result=process.in.text


html=
&quot;&quot;&quot;
&lt;p&gt;
  &lt;textarea type=&quot;text&quot; style=&quot;width:700px;height:400px;&quot; name=&quot;value&quot; &gt;${result}&lt;/textarea&gt;
&lt;/p&gt;
&quot;&quot;&quot;
return html</script>
              <sandbox>false</sandbox>
            </secureScript>
            <secureFallbackScript plugin="script-security@1.29.1">
              <script></script>
              <sandbox>false</sandbox>
            </secureFallbackScript>
          </script>
          <projectName>ManageDockerfile_Base</projectName>
          <parameters class="linked-hash-map">
            <entry>
              <string>Tenant</string>
              <string>demo4</string>
            </entry>
            <entry>
              <string>EnvName</string>
              <string>qa</string>
            </entry>
            <entry>
              <string>Component</string>
              <string></string>
            </entry>
            <entry>
              <string>NameSpace</string>
              <string>demo4</string>
            </entry>
          </parameters>
          <referencedParameters>Tenant,EnvName,Component,NameSpace</referencedParameters>
          <choiceType>ET_FORMATTED_HTML</choiceType>
          <omitValueField>true</omitValueField>
        </org.biouno.unochoice.DynamicReferenceParameter>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2.36.1">
    <script>pipeline {
    agent none
    stages {
        stage(&apos;Create Dockerfile of Specified Component On Target Env &apos;) {
            agent { label &apos;master&apos; }
            steps {
                script{
                      if(env.Component ==&apos;&apos;){
                         sh &quot;python3.6 /commerce-devops-utilities/scripts/kube/kubcli.py createconfmap -tenant ${Tenant} -env ${EnvName} -name dockerfile -namespace ${NameSpace} -rawconfig &apos;Dockerfile::${Dockerfile}&apos;&quot;
                      }else{
                         sh &quot;python3.6 /commerce-devops-utilities/scripts/kube/kubcli.py createconfmap -tenant ${Tenant} -env ${EnvName} -name ${Component}-dockerfile -namespace ${NameSpace} -rawconfig &apos;Dockerfile::${Dockerfile}&apos;&quot;
                      }
                } 
            }
        }
    }
}</script>
    <sandbox>true</sandbox>
  </definition>
  <triggers/>
  <disabled>false</disabled>
</flow-definition>
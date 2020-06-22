#!/bin/bash
oc delete -f deploy/crds/nodered.com_v1alpha1_noderedconfig_cr.yaml
oc delete -f deploy/crds/nodered.com_v1alpha1_nodered_cr.yaml
oc delete -f deploy/operator.yaml 
operator-sdk build openshift-registry-openshift-image-registry.alkesh-cpd3-192314-915b3b336cabec458a7c7ec2aa7c625f-0000.us-south.containers.appdomain.cloud/node-red-p2/node-red-operator:0.0.3
docker push openshift-registry-openshift-image-registry.alkesh-cpd3-192314-915b3b336cabec458a7c7ec2aa7c625f-0000.us-south.containers.appdomain.cloud/node-red-p2/node-red-operator:0.0.3
oc create -f deploy/operator.yaml
oc create -f deploy/crds/nodered.com_v1alpha1_nodered_cr.yaml
#sleep 30
#oc create -f deploy/crds/nodered.com_v1alpha1_noderedconfig_cr.yaml

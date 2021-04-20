FROM registry.access.redhat.com/ubi8/ubi AS base
MAINTAINER IBM-Edge edge@us.ibm.com

LABEL name="Node Red" \
      maintainer="edge@us.ibm.com" \
      vendor="node-red" \
      version="1.2.8" \
      release="1" \
      summary="Node Red v1.2.8 setup on ubi8" \
      description="Node-RED is a programming tool for wiring together hardware devices, APIs and online services in new and interesting ways."

#Copy license
COPY LICENSE /licenses/license.txt

# Copy scripts
COPY scripts/*.sh /tmp/
RUN chmod 755 /tmp/remove_native_gpio.sh
# Install tools, create Node-RED app and data dir, add user and set rights
RUN set -ex && \
    yum install -y --disableplugin=subscription-manager tzdata iputils nano git openssl openssh-clients && \
    mkdir -p /usr/src/node-red /data && \
    adduser -d /usr/src/node-red -M node-red -u 1000 && \
    chown -R node-red:node-red /data && \
    chown -R node-red:node-red /usr/src/node-red 

# Set work directory
WORKDIR /usr/src/node-red

# package.json contains Node-RED NPM module and node dependencies
COPY package.json .
RUN yum install -y --disableplugin=subscription-manager udev python36 gcc-c++ make cronie
#Install nodejs
RUN curl -sL https://rpm.nodesource.com/setup_12.x | bash -
RUN yum install -y --disableplugin=subscription-manager nodejs

#### Stage BUILD #######################################################################################################
FROM base AS build

# Install Build tools
RUN npm install --unsafe-perm --no-update-notifier --only=production && \
    /tmp/remove_native_gpio.sh && \
    cp -R node_modules prod_node_modules

#### Stage RELEASE #####################################################################################################
FROM base AS RELEASE

COPY --from=build /usr/src/node-red/prod_node_modules ./node_modules

# Chown
RUN chown -R node-red:node-red /usr/src/node-red 
   
USER node-red

# Env variables
ENV NODE_RED_VERSION=1.2.8 \
    NODE_PATH=/usr/src/node-red/node_modules:/data/node_modules \
    FLOWS=flows.json

# ENV NODE_RED_ENABLE_SAFE_MODE=true    # Uncomment to enable safe start mode (flows not running)
ENV NODE_RED_ENABLE_PROJECTS=true     

# User configuration directory volume
VOLUME ["/data"]

# Expose the listening port of node-red
EXPOSE 1880

# Add a healthcheck (default every 30 secs)
# HEALTHCHECK CMD curl http://localhost:1880/ || exit 1

ENTRYPOINT ["npm", "start", "--", "--settings", "/data/usr/conf/settings.js" ]

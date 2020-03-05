/*
 * Copyright (c) 2018, WSO2 Inc. (http://wso2.com) All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.ballerinalang.platform.playground.utils.cmd.dto;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;

import java.lang.reflect.Type;

/**
 * GSON Adaptor for commands
 */
public class CommandAdaptor implements JsonSerializer<Command>, JsonDeserializer<Command> {
    public Command deserialize(JsonElement jsonElement, Type type,
                               JsonDeserializationContext context) throws JsonParseException {
        JsonObject json = jsonElement.getAsJsonObject();
        String command = json.getAsJsonPrimitive("command").getAsString();
        Command cmd;
        switch (command) {
            case "run": cmd = context.deserialize(json, RunCommand.class); break;
            default: cmd = new Command(); cmd.setCommand(command); break;
        }
        return cmd;
    }

    public JsonElement serialize(Command command, Type type, JsonSerializationContext context) {
        if (command instanceof RunCommand) {
            return context.serialize(command, RunCommand.class);
        }
        return context.serialize(command);
    }
}

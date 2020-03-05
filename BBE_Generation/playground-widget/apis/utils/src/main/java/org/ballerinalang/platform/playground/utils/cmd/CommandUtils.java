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
package org.ballerinalang.platform.playground.utils.cmd;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.ballerinalang.platform.playground.utils.cmd.dto.Command;
import org.ballerinalang.platform.playground.utils.cmd.dto.CommandAdaptor;

/**
 * Command Utils
 */
public class CommandUtils {
    private static final Gson gson;

    static {
        GsonBuilder builder = new GsonBuilder();
        builder.registerTypeAdapter(Command.class, new CommandAdaptor());
        gson = builder.create();
    }

    public static Command fromJson(String message) {
        return gson.fromJson(message, Command.class);
    }
}

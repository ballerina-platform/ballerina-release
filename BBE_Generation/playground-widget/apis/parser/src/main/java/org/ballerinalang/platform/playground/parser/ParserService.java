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
package org.ballerinalang.platform.playground.parser;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import io.netty.handler.codec.http.HttpHeaderNames;
import org.ballerinalang.compiler.CompilerPhase;
import org.ballerinalang.langserver.compiler.LSCompiler;
import org.ballerinalang.langserver.compiler.LSCompilerException;
import org.ballerinalang.langserver.compiler.common.modal.BallerinaFile;
import org.ballerinalang.langserver.compiler.common.modal.SymbolMetaInfo;
import org.ballerinalang.langserver.compiler.format.JSONGenerationException;
import org.ballerinalang.langserver.compiler.format.TextDocumentFormatUtil;
import org.ballerinalang.langserver.formatting.FormattingSourceGen;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.wso2.ballerinalang.compiler.tree.BLangCompilationUnit;
import org.wso2.ballerinalang.compiler.tree.BLangNode;
import org.wso2.ballerinalang.compiler.tree.BLangPackage;

import javax.ws.rs.Consumes;
import javax.ws.rs.OPTIONS;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

/**
 * Ballerina Parser Service for playground
 */
@Path("/api/parser")
public class ParserService {

    private static final Logger logger = LoggerFactory.getLogger(ParserService.class);

    @OPTIONS
    @Path("/")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response validateAndParseOptions() {

        return Response.ok()
                .header(HttpHeaderNames.ACCESS_CONTROL_MAX_AGE.toString(), "600 ")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), "*")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_CREDENTIALS.toString(), "true")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_METHODS.toString(),
                        "POST, GET, PUT, UPDATE, DELETE, OPTIONS, HEAD")
                .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_HEADERS.toString(),
                        HttpHeaderNames.CONTENT_TYPE.toString() + ", " + HttpHeaderNames.ACCEPT.toString() +
                                ", X-Requested-With").build();
    }

    @POST
    @Path("/")
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response validateAndParse(ParseRequest request) {
        JsonObject result = new JsonObject();
        Response response = null;
        try {
            result.add("model", getTreeForContent(request.getContent()));
            response = Response.status(Response.Status.OK)
                    .entity(result)
                    .header(HttpHeaderNames.ACCESS_CONTROL_ALLOW_ORIGIN.toString(), '*')
                    .type(MediaType.APPLICATION_JSON)
                    .build();
        } catch (Exception e) {
            response = Response
                    .serverError()
                    .entity(e.getMessage())
                    .build();
            logger.error("Error while validate and parse ", e);
        }
        return response;
    }

    private JsonElement getTreeForContent(String content) throws LSCompilerException, JSONGenerationException {
        System.setProperty("experimental", "true");
        BallerinaFile ballerinaFile = LSCompiler.compileContent(content, CompilerPhase.CODE_ANALYZE);
        Optional<BLangPackage> bLangPackage = ballerinaFile.getBLangPackage();
        SymbolFindVisitor symbolFindVisitor = new SymbolFindVisitor(ballerinaFile.getCompilerContext());

        if (bLangPackage.isPresent() && bLangPackage.get().symbol != null) {
            symbolFindVisitor.visit(bLangPackage.get());
            Map<BLangNode, List<SymbolMetaInfo>> symbolMetaInfoMap = symbolFindVisitor.getVisibleSymbolsMap();
            BLangCompilationUnit compilationUnit = bLangPackage.get().getCompilationUnits().stream()
                    .findFirst()
                    .orElse(null);
            JsonElement jsonAST = TextDocumentFormatUtil.generateJSON(compilationUnit, new HashMap<>(),
                    symbolMetaInfoMap);
            FormattingSourceGen.build(jsonAST.getAsJsonObject(), "CompilationUnit");
            return jsonAST;
        }
        return null;
    }


    class ParseRequest {
        private String content;

        public String getContent() {
            return content;
        }

        public void setContent(String content) {
            this.content = content;
        }
    }
}

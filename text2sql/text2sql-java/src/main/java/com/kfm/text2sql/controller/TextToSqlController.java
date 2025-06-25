package com.kfm.text2sql.controller;

import com.kfm.text2sql.model.SqlResponse;
import com.kfm.text2sql.model.UserRequest;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.ChatOptions;
import org.springframework.dao.DataAccessException;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class TextToSqlController {
    private final ChatClient ai;
    private final JdbcTemplate db;

    public TextToSqlController(ChatClient ai, JdbcTemplate db) {
        this.ai = ai; this.db = db;
    }

    @PostMapping("/text2sql")
    public SqlResponse text2sql(@RequestBody UserRequest req) {
        var message = "为这个问题生成 SQL: " + req.getQuestion()
                + "\n数据库 schema: users(id,name,age), orders(id,user_id,amount). 仅返回 SQL。";
        String sql = ai.prompt().user(message).call().content();
        System.out.println( sql);
        // 如果sql 中包含 ```sql 或 ``` 则去掉
        if (sql.contains("```sql") || sql.contains("```")) {
            sql = sql.replace("```sql", "").replace("```", "");
        }   
        List<Map<String,Object>> result = db.queryForList(sql);
        return new SqlResponse(sql, result);
    }

    @PostMapping("/text2sql2")
    public ResponseEntity<?> convert(@RequestBody UserRequest req){
        var prompt = "为y用户的问题生成 SQL。 \n数据库 schema: users(id,name,age), orders(id,user_id,amount). 仅返回 SQL。";
        String sql = ai.prompt(prompt).user(req.getQuestion()).options(ChatOptions.builder().model("gpt-4o").temperature(.0).build()).call().content();
        System.out.println( sql);
        // 如果sql 中包含 ```sql 或 ``` 则去掉
        if (sql.contains("```sql") || sql.contains("```")) {
            sql = sql.replace("```sql", "").replace("```", "");
        }
        List<Map<String,Object>> data;
        try {
            data = db.queryForList(sql);
        } catch (DataAccessException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "SQL 错误: " + e.getMessage());
        }
        return ResponseEntity.ok(new SqlResponse(sql, data));
    }
}


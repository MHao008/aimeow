package com.kfm.text2sql.model;

import lombok.Data;

import java.util.HashMap;

public class SqlResponse extends HashMap<String, Object> {

    public SqlResponse(String sql, Object result) {
        put("sql", sql);
        put("result", result);
    }
}

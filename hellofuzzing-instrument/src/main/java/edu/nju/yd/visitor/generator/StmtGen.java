package edu.nju.yd.visitor.generator;

import com.github.javaparser.ast.stmt.ExpressionStmt;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.visitor.generator
 * @className: StmtGen
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 11:03
 * @version: 1.0
 */
public class StmtGen {
    public static ExpressionStmt GenExpressionStmt(String s){
        ExpressionStmt expressionStmt = new ExpressionStmt();
        expressionStmt.setExpression(s);
        return expressionStmt;
    }

    // generate statement that changes the cov_info
    // result like:
    // cov_info[2] = '1';
    public static ExpressionStmt GenCovInfoChangeStatement(int num){
        String s = "cov_info["+num+"] = '1'";
        ExpressionStmt expressionStmt = new ExpressionStmt();
        expressionStmt.setExpression(s);
        return expressionStmt;
    }

    public static ExpressionStmt GenPrintCovArrayStatement(){
        return GenExpressionStmt("System.out.print(\"\\n\"+ new String(cov_info))");
    }
}

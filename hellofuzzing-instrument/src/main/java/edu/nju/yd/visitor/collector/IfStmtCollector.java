package edu.nju.yd.visitor.collector;

import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.List;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.visitor.collector
 * @className: IfStmtCollector
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 9:43
 * @version: 1.0
 */
public class IfStmtCollector extends VoidVisitorAdapter<List<IfStmt>> {
    @Override
    public void visit(IfStmt ifStmt,List<IfStmt> ifStmtList){
        super.visit(ifStmt,ifStmtList);
        ifStmtList.add(ifStmt);
    }
}

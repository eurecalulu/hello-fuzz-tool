package edu.nju.yd.visitor.generator;

import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.stmt.BlockStmt;
import com.github.javaparser.ast.stmt.Statement;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.visitor.generator
 * @className: BlockStmtGen
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 11:01
 * @version: 1.0
 */
public class BlockStmtGen {
    public static BlockStmt blockGenFromStmts(NodeList<Statement> statements){
        return new BlockStmt(statements);
    }
}

package edu.nju.yd.components;

import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.stmt.*;
import edu.nju.yd.visitor.collector.IfStmtCollector;
import edu.nju.yd.visitor.collector.SwitchEntryCollector;
import edu.nju.yd.visitor.generator.BlockStmtGen;
import edu.nju.yd.visitor.generator.StmtGen;

import java.util.ArrayList;
import java.util.List;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.components
 * @className: IfStmts
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 10:07
 * @version: 1.0
 */
public class Branches {
    private List<IfStmt> ifElseStmts = new ArrayList<>();
    private List<BlockStmt> ifStmts = new ArrayList<>();
    private List<BlockStmt> elseStmts = new ArrayList<>();
    private List<SwitchEntry> switchEntries = new ArrayList<>();

    private int num;
    public Branches(CompilationUnit cu){
        // get if-else
        IfStmtCollector ifStmtCollector = new IfStmtCollector();
        ifStmtCollector.visit(cu,this.ifElseStmts);
        // change one statement to block statement and get if statement and else statement respectively
        changeOneStmtToBlock();
        //get switch entries
        SwitchEntryCollector switchEntryCollector = new SwitchEntryCollector();
        switchEntryCollector.visit(cu,this.switchEntries);
        this.num = ifStmts.size()+elseStmts.size()+switchEntries.size();
    }

    public void insertStatement(){
        int flag = 0;
        for(BlockStmt ifStmt: this.ifStmts){
            ifStmt.addStatement(0, StmtGen.GenCovInfoChangeStatement(flag++));
        }
        for(BlockStmt elseStmt: this.elseStmts){
            elseStmt.addStatement(0,StmtGen.GenCovInfoChangeStatement(flag++));
        }
        for(SwitchEntry switchEntry:this.switchEntries){
            switchEntry.addStatement(0,StmtGen.GenCovInfoChangeStatement(flag++));
        }
    }

    private void changeOneStmtToBlock(){
        for(IfStmt ifStmt: ifElseStmts){
            Statement thenStmt = ifStmt.getThenStmt();
            if(!(thenStmt instanceof BlockStmt)){
                NodeList<Statement> statements = new NodeList<>();
                statements.add(thenStmt);
                ifStmt.setThenStmt(BlockStmtGen.blockGenFromStmts(statements));
            }
            ifStmts.add(ifStmt.getThenStmt().asBlockStmt());
            boolean hasElseStmt = ifStmt.getElseStmt().isPresent();
            if(hasElseStmt){
                Statement elseStmt = ifStmt.getElseStmt().get();
                if(!(elseStmt instanceof BlockStmt)){
                    NodeList<Statement> statements = new NodeList<>();
                    statements.add(elseStmt);
                    ifStmt.setElseStmt(BlockStmtGen.blockGenFromStmts(statements));
                }
                elseStmts.add(ifStmt.getElseStmt().get().asBlockStmt());
            }
        }
    }

    public int getNum(){
        return this.num;
    }
}

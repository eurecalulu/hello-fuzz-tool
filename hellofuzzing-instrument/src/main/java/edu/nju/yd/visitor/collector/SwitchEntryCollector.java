package edu.nju.yd.visitor.collector;

import com.github.javaparser.ast.stmt.IfStmt;
import com.github.javaparser.ast.stmt.SwitchEntry;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.List;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.visitor.collector
 * @className: SwitchEntryCollector
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 11:26
 * @version: 1.0
 */
public class SwitchEntryCollector extends VoidVisitorAdapter<List<SwitchEntry>> {
    @Override
    public void visit(SwitchEntry switchEntry, List<SwitchEntry> switchEntryList){
        super.visit(switchEntry,switchEntryList);
        switchEntryList.add(switchEntry);
    }
}

package edu.nju.yd.visitor.collector;

import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.visitor.VoidVisitorAdapter;

import java.util.List;

public class ClassOrInterfaceDeclarationCollector extends VoidVisitorAdapter<List<ClassOrInterfaceDeclaration>> {
    @Override
    public void visit(ClassOrInterfaceDeclaration classOrInterfaceDeclaration, List<ClassOrInterfaceDeclaration> collector){
        super.visit(classOrInterfaceDeclaration,collector);
        collector.add(classOrInterfaceDeclaration);
    }
}

package edu.nju.yd;

import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Modifier;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.body.MethodDeclaration;
import com.github.javaparser.ast.expr.ArrayInitializerExpr;
import com.github.javaparser.ast.expr.CharLiteralExpr;
import com.github.javaparser.printer.PrettyPrinter;
import edu.nju.yd.components.Branches;
import edu.nju.yd.util.IOUtil;
import edu.nju.yd.visitor.collector.ClassOrInterfaceDeclarationCollector;
import edu.nju.yd.visitor.collector.MethodDeclarationCollector;
import edu.nju.yd.visitor.generator.StmtGen;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd
 * @className: HelloFuzzingInstrument
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 9:29
 * @version: 1.0
 */
public class HelloFuzzingInstrument {
    public static CompilationUnit cu;
    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.out.println("Usage: java -jar theTar.jar <targetPath>");
            return;
        }

//        String fuzzTargetPath = "E:\\y1\\software-testing\\code\\fuzz-mut-demos\\fuzz-targets\\edu\\nju\\isefuzz\\trgt\\Target1.java";
        String fuzzTargetPath = args[0];
        File fuzzTarget = new File(fuzzTargetPath);
        // initialize cu
        cu = StaticJavaParser.parse(fuzzTarget);
        // get all branches
        Branches branches = new Branches(cu);
        // insert char[] cov_info declaration
        IOUtil.consoleMessage("insert char[] cov_info declaration...");
        insertCovInfoArray(branches.getNum());
        // insert statement that modify cov_info
        IOUtil.consoleMessage("insert statements that modify cov_info...");
        branches.insertStatement();
        // insert statement to output the cov_info of this run
        IOUtil.consoleMessage("insert print statement in the end...");
        insertOutPutStmt();
        // 创建新的java文件
        createNewJavaFile(fuzzTarget);
    }

    public static void insertCovInfoArray(int num){
        ClassOrInterfaceDeclarationCollector collector = new ClassOrInterfaceDeclarationCollector();
        List<ClassOrInterfaceDeclaration> declarations = new ArrayList<>();
        collector.visit(cu,declarations);
        ClassOrInterfaceDeclaration theClass = declarations.get(0);
        NodeList charLiteralExprs = new NodeList();
        for(int i =0;i<num;i++){
            charLiteralExprs.add(new CharLiteralExpr('0'));
        }
        theClass.addFieldWithInitializer("char[]","cov_info",new ArrayInitializerExpr(charLiteralExprs), Modifier.publicModifier().getKeyword(),Modifier.staticModifier().getKeyword());
        // btw, change class name
        String nameBefore = theClass.getNameAsString();
        theClass.setName(nameBefore+"HelloFuzzing");
    }

    public static void insertOutPutStmt(){
        MethodDeclarationCollector collector = new MethodDeclarationCollector();
        List<MethodDeclaration> methodDeclarations = new ArrayList<>();
        collector.visit(cu,methodDeclarations);
        MethodDeclaration mainEntry = null;
        for(MethodDeclaration methodDeclaration:methodDeclarations){
            if(methodDeclaration.getNameAsString().equals("main")){
                mainEntry = methodDeclaration;
            }
        }
        mainEntry.getBody().ifPresent(blockStmt -> {
            blockStmt.addStatement(StmtGen.GenPrintCovArrayStatement());
        });
    }

    public static void createNewJavaFile(File fuzz_target) throws IOException {
        String parentPath = fuzz_target.getParent();
        String newJavaPath = parentPath + File.separator + fuzz_target.getName().split("\\.")[0]+"HelloFuzzing.java";
        IOUtil.createNewFileWithContent(newJavaPath,new PrettyPrinter().print(cu));
    }
}

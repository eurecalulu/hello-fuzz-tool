package edu.nju.yd.util;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * @projectName: hellofuzzing-instrument
 * @package: edu.nju.yd.util
 * @className: IOUtil
 * @author: Yang Ding
 * @description:
 * @date: 2023/12/14 12:30
 * @version: 1.0
 */
public final class IOUtil {
    private IOUtil(){}

    public static void createNewFileWithContent(String filePath, String content) throws IOException {
        File file = new File(filePath);

        if (file.exists()) {
            if (file.delete()) {
                consoleMessage("File deleted successfully.");
            } else {
                consoleMessage("Failed to delete the file.");
            }
        } else {
            consoleMessage("File doesn't exist.");
        }

        if(file.createNewFile()){
            consoleMessage("create file successfully!");
        } else {
            consoleMessage("file create failed.");
        }

        try (FileWriter writer = new FileWriter(file)) {
            writer.write(content);
        }
        consoleMessage("output to: "+filePath);
    }

    public static void consoleMessage(String s){
        System.out.println("[hellofuzzing-instrument]"+s);
    }
}

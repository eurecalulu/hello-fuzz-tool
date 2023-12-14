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
                System.out.println("File deleted successfully.");
            } else {
                System.out.println("Failed to delete the file.");
            }
        } else {
            System.out.println("File doesn't exist.");
        }

        if(file.createNewFile()){
            System.out.println("create file successfully!");
        } else {
            System.out.println("file create failed.");
        }

        try (FileWriter writer = new FileWriter(file)) {
            writer.write(content);
        }
        System.out.println("output to: "+filePath);
    }
}

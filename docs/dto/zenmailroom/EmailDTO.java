package it.interzen.zencommonlibrary.dto.zenmailroom;

import lombok.Data;

import java.util.HashMap;
import java.util.Map;

@Data
public class EmailDTO {
    private Long emailparameterid;
    private String from;
    private String[] to;
    private String[] cc = new String[0];
    private String[] bcc = new String[0];
    private String subject;
    private String body;
    private String[] attachment = new String[0];
    private Map<String,String> base64attachment = new HashMap<>();
}

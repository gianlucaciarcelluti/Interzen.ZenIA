package it.interzen.zencommonlibrary.dto.zenprocess.form;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class ZenProcessFormDTO {
    List<FormComponent> components;
    WebFormCompleteModeEnum formCompleteMode = WebFormCompleteModeEnum.SINGLE;
    String type = "default";
    String id;
    Exporter exporter;
    int schemaVersion = 17;
}

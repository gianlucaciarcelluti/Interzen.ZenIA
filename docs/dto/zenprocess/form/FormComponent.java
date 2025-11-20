package it.interzen.zencommonlibrary.dto.zenprocess.form;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;
import java.util.Map;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonInclude(JsonInclude.Include.NON_NULL)
public class FormComponent {
    // standard fields
    String id;
    String key;
    String label;
    Layout layout;
    String text;
    String type;
    List<Value> values;
    Conditional conditional;
    Validate validate;
    Boolean readonly;
    Boolean disabled;

    // Date
    String dateLabel;
    String subtype;

    // Select
    String valuesExpression;

    // Expression
    String computeOn;

    // File Picker
    String accept;
    String multiple;

    // Table
    List<Column> columns;
    String dataSource;
    Integer rowCount;

    // Html
    String content;

    // Image
    String source;

    // Document preview
    String endpointKey;

    // Spacer
    Integer height;

    // Group
    List<FormComponent> components;
    Boolean showOutline;

    // Dynamiclist
    Boolean allowAddRemove;
    Integer defaultRepetitions;
    Boolean isRepeating;
    String path;

    // Iframe
    Security security;

    // Quill Editor
    Object defaultValue;
    Editors editors;

    // Custom Button
    String action;
    Map<String, String> properties;

    @Data
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class Value {
        private String label;
        private String value;
    }
}

package it.interzen.zencommonlibrary.dto.zenprocess.form;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.annotation.Nullable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class Validate {
    Boolean required = false;
    @Nullable
    Integer minLength;
    @Nullable
    Integer maxLength;
    @Nullable
    String pattern;
}

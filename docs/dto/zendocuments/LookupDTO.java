package it.interzen.zencommonlibrary.dto.zendocuments;

import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class LookupDTO {
    private Long id;

    private String description;
}

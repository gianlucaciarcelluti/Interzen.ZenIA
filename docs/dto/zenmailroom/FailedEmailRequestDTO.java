package it.interzen.zencommonlibrary.dto.zenmailroom;

import lombok.Data;

import java.time.LocalDateTime;

@Data
public class FailedEmailRequestDTO {
    String searchKeyword;
    LocalDateTime startDate = LocalDateTime.now().minusDays(7);
    LocalDateTime endDate = LocalDateTime.now();
}

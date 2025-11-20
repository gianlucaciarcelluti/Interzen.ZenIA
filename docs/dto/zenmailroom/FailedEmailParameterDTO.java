package it.interzen.zencommonlibrary.dto.zenmailroom;

import java.time.LocalDateTime;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * @author Gianluca Ciarcelluti
 */

@Data
@AllArgsConstructor
@NoArgsConstructor
public class FailedEmailParameterDTO {
	private Long id;
	private String description;
	private String emailaddress;
	private String username;
	private Integer emailtype;
	private String errorDescription;
	private LocalDateTime errorData;
}
package it.interzen.zencommonlibrary.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FilterDTO {
	private String field;
	private String operator;
	private String[] values;
	
}

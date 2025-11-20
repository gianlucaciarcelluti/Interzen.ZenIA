package it.interzen.zencommonlibrary.dto.zenprotocollo;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ProtocolListOperationsDTO {
	
	private boolean view = true;
	private boolean edit = true;
	private boolean delete = true;

}

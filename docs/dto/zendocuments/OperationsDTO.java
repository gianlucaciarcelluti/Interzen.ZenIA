package it.interzen.zencommonlibrary.dto.zendocuments;

import lombok.Data;

/**
 * Identifica il DTO con le proprietà di base per i documenti.
 * Gli altri DTO estendono questa classe
 */
@Data
public class OperationsDTO {
	protected Boolean view = false;
	protected Boolean create = false;
	protected Boolean edit = false;
	protected Boolean delete = false;
}

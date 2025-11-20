package it.interzen.zencommonlibrary.dto.zendocuments;

import java.math.BigDecimal;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DiskInfoDTO {
	private BigDecimal diskusedGB;
	private BigDecimal diskusedDeletedGB; // Cestino
	private BigDecimal diskavailableGB;
	private Long documentCount;
	private Long documentDeletedCount;  // Cestino
}

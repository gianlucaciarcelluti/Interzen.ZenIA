package it.interzen.zencommonlibrary.dto.zendocuments.smistamento;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.AssertTrue;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class AssigneeCreateDTO {
	
	
    /**
     * The ID of the group.
     */
    @Schema(description = "The ID of the group.")
    private Long groupId;

    /**
     * The ID of the user.
     */
    @Schema(description = "The ID of the user.")
    private Long userId;

    /**
     * The type of the assignment.
     */
    @Schema(description = "The type of the assignment.")
    @NotNull(message = "The type field is required.")
    private AssignmentSlaveType type;

    /**
     * Whether to send an email notification.
     * TODO: Da definire in futuro
     */
    @Schema(description = "Whether to send an email notification.")
    private boolean emailNotification = true;
	
	
    
    
    
	@AssertTrue(message = "Either groupId or userId must have a value, but not both.")
    public boolean onlyOneIdHasValue() {
        return (groupId != null && userId == null) || (groupId == null && userId != null);
    }

}

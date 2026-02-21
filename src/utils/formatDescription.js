/**
 * Utility to parse quest/reward tags in talent/ability descriptions
 * and convert them to HTML with appropriate styling.
 * 
 * Usage in Vue component:
 * <span v-html="formatDescription(talent.description)"></span>
 */

export function formatDescription(description) {
  if (!description) return '';
  
  let formatted = description;
  
  // Escape HTML to prevent XSS
  formatted = formatted
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  
  // Replace {quest}...{/quest} with styled span (blue/cyan)
  formatted = formatted.replace(
    /\{quest\}(.+?)\{\/quest\}/g,
    '<span class="quest-tag">$1</span>'
  );
  
  // Replace {reward}...{/reward} with styled span (blue/cyan)
  formatted = formatted.replace(
    /\{reward\}(.+?)\{\/reward\}/g,
    '<span class="quest-tag">$1</span>'
  );
  
  // Replace {mythic}...{/mythic} with styled span (purple)
  formatted = formatted.replace(
    /\{mythic\}(.+?)\{\/mythic\}/g,
    '<span class="mythic-tag">$1</span>'
  );
  
  // Replace {mythic_reward}...{/mythic_reward} with styled span (purple)
  formatted = formatted.replace(
    /\{mythic_reward\}(.+?)\{\/mythic_reward\}/g,
    '<span class="mythic-tag">$1</span>'
  );
  
  // Replace newlines with <br> if needed
  formatted = formatted.replace(/\n/g, '<br>');
  
  return formatted;
}

/**
 * Alternative: Split description into segments for safer rendering
 * Usage:
 * <template v-for="(segment, idx) in parseDescription(talent.description)" :key="idx">
 *   <span v-if="segment.type === 'text'">{{ segment.content }}</span>
 *   <span v-else-if="segment.type === 'quest'" class="quest-tag">{{ segment.content }}</span>
 *   <span v-else-if="segment.type === 'mythic'" class="mythic-tag">{{ segment.content }}</span>
 * </template>
 */
export function parseDescription(description) {
  if (!description) return [{ type: 'text', content: '' }];
  
  const segments = [];
  const regex = /\{(quest|reward|mythic|mythic_reward)\}(.+?)\{\/\1\}/g;
  let lastIndex = 0;
  let match;
  
  while ((match = regex.exec(description)) !== null) {
    // Add text before the tag
    if (match.index > lastIndex) {
      segments.push({
        type: 'text',
        content: description.slice(lastIndex, match.index)
      });
    }
    
    // Add the tagged segment
    segments.push({
      type: match[1] === 'reward' ? 'quest' : match[1] === 'mythic_reward' ? 'mythic' : match[1], // 'quest' or 'mythic'
      content: match[2]
    });
    
    lastIndex = match.index + match[0].length;
  }
  
  // Add remaining text
  if (lastIndex < description.length) {
    segments.push({
      type: 'text',
      content: description.slice(lastIndex)
    });
  }
  
  return segments;
}

<template>
  <div class="page-editor">
    <div class="editor-card">
      <h3 class="editor-title">飞书通知</h3>
      <div class="field-grid">
        <label class="field"><span>飞书模式</span>
          <select :value="modelValue?.feishuMode || 'app'" @change="update('feishuMode', $event.target.value)">
            <option value="app">应用模式（交互卡片）</option>
            <option value="webhook">Webhook 模式</option>
          </select>
        </label>
        <label class="field full"><span>Webhook URL</span><input :value="modelValue?.feishuWebhookUrl || ''" @input="update('feishuWebhookUrl', $event.target.value)" placeholder="https://open.feishu.cn/open-apis/bot/v2/hook/..." /></label>
        <label class="field"><span>App ID</span><input :value="modelValue?.feishuAppId || ''" @input="update('feishuAppId', $event.target.value)" placeholder="cli_xxxxx" /></label>
        <label class="field"><span>App Secret</span><input type="password" :value="modelValue?.feishuAppSecret || ''" @input="update('feishuAppSecret', $event.target.value)" /></label>
        <label class="field full"><span>Chat ID</span><input :value="modelValue?.feishuAppChatId || ''" @input="update('feishuAppChatId', $event.target.value)" placeholder="oc_xxxxx" /></label>
        <label class="field"><span>Verification Token</span><input :value="modelValue?.feishuAppVerificationToken || ''" @input="update('feishuAppVerificationToken', $event.target.value)" /></label>
        <label class="field"><span>Encrypt Key</span><input type="password" :value="modelValue?.feishuAppEncryptKey || ''" @input="update('feishuAppEncryptKey', $event.target.value)" /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">邮件发送</h3>
      <div class="field-grid">
        <label class="field"><span>启用邮件</span>
          <select :value="modelValue?.mailEnabled ? 'true' : 'false'" @change="update('mailEnabled', $event.target.value === 'true')">
            <option value="false">关闭</option>
            <option value="true">开启</option>
          </select>
        </label>
        <label class="field"><span>SMTP 端口</span><input type="number" :value="modelValue?.smtpPort || 587" @input="update('smtpPort', parseInt($event.target.value) || 587)" /></label>
        <label class="field full"><span>SMTP 服务器</span><input :value="modelValue?.smtpHost || ''" @input="update('smtpHost', $event.target.value)" placeholder="smtp.example.com" /></label>
        <label class="field"><span>SMTP 用户名</span><input :value="modelValue?.smtpUsername || ''" @input="update('smtpUsername', $event.target.value)" /></label>
        <label class="field"><span>SMTP 密码</span><input type="password" :value="modelValue?.smtpPassword || ''" @input="update('smtpPassword', $event.target.value)" /></label>
        <label class="field"><span>发件人邮箱</span><input :value="modelValue?.mailFromEmail || ''" @input="update('mailFromEmail', $event.target.value)" placeholder="noreply@example.com" /></label>
        <label class="field"><span>发件人名称</span><input :value="modelValue?.mailFromName || '星雨作坊'" @input="update('mailFromName', $event.target.value)" /></label>
        <label class="field"><span>使用 SSL</span>
          <select :value="modelValue?.smtpUseSsl ? 'true' : 'false'" @change="update('smtpUseSsl', $event.target.value === 'true')">
            <option value="false">关闭</option>
            <option value="true">开启</option>
          </select>
        </label>
        <label class="field"><span>使用 TLS</span>
          <select :value="modelValue?.smtpUseTls ? 'true' : 'false'" @change="update('smtpUseTls', $event.target.value === 'true')">
            <option value="false">关闭</option>
            <option value="true">开启</option>
          </select>
        </label>
        <label class="field full"><span>群聊邀请链接（通过后邮件附带）</span><input :value="modelValue?.groupChatInviteLink || ''" @input="update('groupChatInviteLink', $event.target.value)" placeholder="https://..." /></label>
      </div>
    </div>

    <div class="editor-card">
      <h3 class="editor-title">站点信息</h3>
      <div class="field-grid">
        <label class="field full"><span>站点图标 URL</span><input :value="modelValue?.siteIcon || ''" @input="update('siteIcon', $event.target.value)" /></label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ modelValue: Object })
const emit = defineEmits(['update:modelValue'])

function update(key, value) {
  emit('update:modelValue', { ...props.modelValue, [key]: value })
}
</script>

<style scoped>
.page-editor { display: flex; flex-direction: column; gap: 20px; }
.editor-card { background: var(--bg-soft); border: 1px solid var(--glass-border); border-radius: var(--radius-md); padding: 20px; }
.editor-title { font-family: var(--font-heading); font-size: 14px; font-weight: 600; margin: 0 0 12px; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.field.full { grid-column: 1 / -1; }
.field span { display: block; font-size: 11px; font-weight: 500; color: var(--text-muted); margin-bottom: 3px; }
.field input, .field textarea, .field select { width: 100%; padding: 7px 10px; border: 1px solid var(--glass-border); border-radius: 6px; font-size: 12px; background: white; color: var(--text-primary); }
.field input:focus, .field textarea:focus, .field select:focus { outline: none; border-color: var(--warm-terracotta); }

@media (max-width: 768px) {
  .editor-card { padding: 12px; }
  .field-grid { grid-template-columns: 1fr; }
}
</style>

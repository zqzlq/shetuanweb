<template>
  <div class="rm-root">
    <!-- 头部统计卡片 -->
    <div class="rm-stats-row">
      <button v-for="s in statuses" :key="s.key" class="rm-stat-card" :class="{ active: activeStatus===s.key }" @click="activeStatus=s.key;page=1;loadResources()">
        <span class="rm-stat-num">{{ counts[s.key] ?? '...' }}</span>
        <span class="rm-stat-label">{{ s.label }}</span>
        <div v-if="activeStatus===s.key" class="rm-stat-bar"></div>
      </button>
      <div class="rm-stat-card brand">
        <span class="rm-stat-num">{{ counts.all ?? '...' }}</span>
        <span class="rm-stat-label">文件/文件夹</span>
        <div class="rm-stat-bar"></div>
      </div>
    </div>

    <!-- 工具栏 -->
    <div class="rm-toolbar">
      <div class="rm-search-wrap">
        <svg class="rm-search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
        <input v-model="search" @input="debouncedLoad" placeholder="搜索..." class="rm-search" />
      </div>
      <div class="rm-actions">
        <button class="rm-btn outline" @click="showUpload=true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg> 上传</button>
        <button class="rm-btn outline" @click="showCreateFolder=true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg> 文件夹</button>
        <button class="rm-btn outline" @click="showTrash=true;loadTrash()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg> 回收站</button>
        <button class="rm-btn outline" @click="showLogs=true;loadLogs()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 日志</button>
      </div>
    </div>

    <!-- 面包屑 -->
    <div class="rm-breadcrumb" v-if="breadcrumb.length||currentFolder">
      <button class="rm-bc-link" @click="navigateTo(null)"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg> 根目录</button>
      <template v-for="item in breadcrumb" :key="item.id">
        <svg class="rm-bc-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
        <button class="rm-bc-link active" @click="navigateTo(item.id)">{{ item.name }}</button>
      </template>
    </div>

    <!-- 批量操作栏 -->
    <div v-if="selectedIds.size>0" class="rm-batch">
      <div class="rm-batch-badge">{{ selectedIds.size }}</div>
      <span class="rm-batch-text">项已选择</span>
      <button class="rm-btn outline red" @click="batchAction('delete')">批量删除</button>
      <button class="rm-btn text" @click="selectedIds.clear()">取消</button>
    </div>

    <!-- 加载/空 -->
    <div v-if="loading" class="rm-loading"><div class="rm-spinner"></div> 加载中...</div>
    <div v-else-if="!items.length" class="rm-empty">暂无内容</div>

    <!-- 列表 -->
    <div v-else class="rm-list">
      <div v-for="item in items" :key="item.id" class="rm-row" :class="{ folder:item.is_folder, selected:selectedIds.has(item.id) }" @click="item.is_folder?navigateTo(item.id):null">
        <div class="rm-cb" @click.stop><input type="checkbox" :checked="selectedIds.has(item.id)" @change="toggleSelect(item.id)" /></div>
        <div class="rm-icon" v-html="item.is_folder?iconFolder():iconFile(item.file_ext)"></div>
        <div class="rm-info">
          <div class="rm-row-top">
            <strong class="rm-name">{{ item.original_name || item.name }}</strong>
            <span class="rm-badge" :class="'badge-'+item.status">{{ statusLabel(item.status) }}</span>
          </div>
          <div class="rm-row-meta">
            <span v-if="item.folder_path" class="rm-folder-path">📁 {{ item.folder_path }}</span>
            <span>{{ formatDate(item.updated_at||item.created_at) }}</span>
            <span v-if="!item.is_folder">{{ formatSize(item.file_size) }}</span>
            <span>{{ item.uploader_name||'-' }}</span>
            <span v-if="!item.is_folder">下载 {{ item.download_count }}</span>
            <span v-if="item.tags?.length">🏷 {{ item.tags.join(', ') }}</span>
          </div>
        </div>
        <div class="rm-row-actions" @click.stop>
          <button v-if="item.is_folder" class="rm-icon-btn" title="进入" @click="navigateTo(item.id)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></button>
          <button class="rm-icon-btn" title="移动" @click="openMove(item.id)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 9-3 3 3 3M9 5l3-3 3 3M15 19l-3 3-3-3M19 9l3 3-3 3M2 12h20M12 2v20"/></svg></button>
          <button class="rm-icon-btn red" title="删除" @click="deleteSingle(item)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="totalPages>1" class="rm-pagination">
      <button class="rm-page-btn" :disabled="page<=1" @click="page--;loadResources()"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg> 上页</button>
      <span class="rm-page-info">{{ page }} / {{ totalPages }}</span>
      <button class="rm-page-btn" :disabled="page>=totalPages" @click="page++;loadResources()">下页 <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg></button>
    </div>

    <!-- 上传弹窗 -->
    <Teleport to="body"><div v-if="showUpload" class="rm-modal-mask" @click.self="showUpload=false"><div class="rm-modal">
      <div class="rm-modal-hd"><h3>上传资源</h3><button class="rm-modal-x" @click="showUpload=false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
      <div class="rm-modal-bd">
        <div class="rm-dropzone" :class="{on:uploadDragover}" @drop.prevent="handleUploadDrop" @dragover.prevent="uploadDragover=true" @dragleave="uploadDragover=false" @click="$refs.fileInput.click()">
          <input ref="fileInput" type="file" @change="handleFileSelect" style="display:none" />
          <template v-if="uploadFile"><strong>{{ uploadFile.name }}</strong><span class="text-muted">{{ formatSize(uploadFile.size) }}</span></template>
          <template v-else><svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/></svg><span>拖拽或点击选择文件</span></template>
        </div>
        <div class="rm-fields">
          <label class="rm-field"><span>标签</span><input v-model="uploadForm.tags" placeholder="逗号分隔" /></label>
          <label class="rm-field full"><span>描述</span><textarea v-model="uploadForm.description" rows="2"></textarea></label>
        </div>
      </div>
      <div class="rm-modal-ft"><button class="rm-btn outline" @click="showUpload=false">取消</button><button class="rm-btn primary" @click="handleUpload" :disabled="!uploadFile||uploading">{{ uploading?'上传中...':'上传' }}</button></div>
    </div></div></Teleport>

    <!-- 文件夹弹窗 -->
    <Teleport to="body"><div v-if="showCreateFolder" class="rm-modal-mask" @click.self="showCreateFolder=false"><div class="rm-modal rm-modal-sm">
      <div class="rm-modal-hd"><h3>新建文件夹</h3><button class="rm-modal-x" @click="showCreateFolder=false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
      <div class="rm-modal-bd"><label class="rm-field"><span>名称</span><input v-model="folderName" placeholder="文件夹名..." @keyup.enter="handleCreateFolder" /></label></div>
      <div class="rm-modal-ft"><button class="rm-btn outline" @click="showCreateFolder=false">取消</button><button class="rm-btn primary" @click="handleCreateFolder" :disabled="!folderName.trim()">创建</button></div>
    </div></div></Teleport>

    <!-- 移动弹窗 -->
    <Teleport to="body"><div v-if="moveTarget!==null" class="rm-modal-mask" @click.self="moveTarget=null"><div class="rm-modal rm-modal-sm">
      <div class="rm-modal-hd"><h3>移动到</h3><button class="rm-modal-x" @click="moveTarget=null"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
      <div class="rm-modal-bd">
        <div class="rm-move-label">目标位置</div>
        <div class="rm-move-tree">
          <div class="rm-move-item" :class="{ active: moveParentId==='' }" @click="moveParentId=''">
            <span class="rm-move-icon">🏠</span><span>根目录</span>
          </div>
          <div v-for="f in sortedFolders" :key="f.id" class="rm-move-item" :class="{ active: moveParentId===f.id }" :style="{ paddingLeft: 14 + f.depth * 22 + 'px' }" @click="moveParentId=f.id">
            <span class="rm-move-icon">{{ f.hasChildren ? '📂' : '📁' }}</span><span>{{ f.name }}</span>
          </div>
        </div>
      </div>
      <div class="rm-modal-ft"><button class="rm-btn outline" @click="moveTarget=null">取消</button><button class="rm-btn primary" @click="handleMove">移动</button></div>
    </div></div></Teleport>

    <!-- 回收站 -->
    <Teleport to="body"><div v-if="showTrash" class="rm-modal-mask" @click.self="showTrash=false"><div class="rm-modal rm-modal-lg">
      <div class="rm-modal-hd"><h3>回收站</h3><button class="rm-modal-x" @click="showTrash=false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
      <div class="rm-modal-bd">
        <p v-if="!trashItems.length" class="rm-empty">回收站为空</p>
        <div v-else class="rm-simple-list">
          <div v-for="it in trashItems" :key="it.id" class="rm-simple-row">
            <span>{{ it.is_folder?'📁':'📄' }}</span>
            <span class="rm-simple-name">{{ it.name }}</span>
            <span class="text-muted">{{ (it.deleted_at||'').slice(0,16).replace('T',' ') }}</span>
            <button class="rm-btn outline sm" @click="restoreItem(it.id)">恢复</button>
            <button class="rm-btn outline red sm" @click="permanentDelete(it.id)">永久删除</button>
          </div>
        </div>
        <div v-if="trashTotalPages>1" class="rm-pagination">
          <button class="rm-page-btn" :disabled="trashPage<=1" @click="trashPage--;loadTrash()">上页</button><span>{{ trashPage }}/{{ trashTotalPages }}</span>
          <button class="rm-page-btn" :disabled="trashPage>=trashTotalPages" @click="trashPage++;loadTrash()">下页</button>
        </div>
      </div>
    </div></div></Teleport>

    <!-- 日志 -->
    <Teleport to="body"><div v-if="showLogs" class="rm-modal-mask" @click.self="showLogs=false"><div class="rm-modal rm-modal-lg">
      <div class="rm-modal-hd"><h3>操作日志</h3><button class="rm-modal-x" @click="showLogs=false"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18M6 6l12 12"/></svg></button></div>
      <div class="rm-modal-bd">
        <p v-if="!logItems.length" class="rm-empty">暂无记录</p>
        <div v-else class="rm-simple-list">
          <div v-for="log in logItems" :key="log.id" class="rm-log-row">
            <span class="rm-log-badge" :class="'lg-'+log.action">{{ actionLabel(log.action) }}</span>
            <span class="rm-log-name">{{ log.resource_name }}</span>
            <span v-if="log.detail" class="text-muted">{{ log.detail }}</span>
            <span>{{ log.user_name||'系统' }}</span>
            <span class="text-muted">{{ (log.created_at||'').slice(0,16).replace('T',' ') }}</span>
          </div>
        </div>
        <div v-if="logTotalPages>1" class="rm-pagination"><button class="rm-page-btn" :disabled="logPage<=1" @click="logPage--;loadLogs()">上页</button><span>{{ logPage }}/{{ logTotalPages }}</span><button class="rm-page-btn" :disabled="logPage>=logTotalPages" @click="logPage++;loadLogs()">下页</button></div>
      </div>
    </div></div></Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getAdminResources, uploadResource, createFolder, deleteResource, updateResourceStatus, batchResources, moveResource, getAdminFolders, getTrash, restoreResource, permanentDeleteResource, getResourceLogs } from '@/services/api'

const statuses=[{key:'',label:'全部'},{key:'approved',label:'已通过'}]
const colors={folder:'#f5a623',pdf:'#e74c3c',doc:'#2b7cd3',docx:'#2b7cd3',xls:'#217346',xlsx:'#217346',ppt:'#d04423',jpg:'#27ae60',jpeg:'#27ae60',png:'#27ae60',gif:'#27ae60',webp:'#27ae60',svg:'#27ae60',zip:'#e67e22',rar:'#e67e22','7z':'#e67e22',py:'#3572a5',js:'#f1e05a',ts:'#3178c6',html:'#e34c26',css:'#563d7c',json:'#292929',txt:'#6b5e52',md:'#6b5e52',mp4:'#9b59b6'}

function iconFolder(){return'<svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M2 6C2 4.9 2.9 4 4 4h5l2 3h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6Z" fill="#f5a623"/></svg>'}
function iconFile(ext){const t=(ext||'').toLowerCase();const c=colors[t]||'#8b7355';let s='F';if(['jpg','jpeg','png','gif','webp','svg'].includes(t))s='🖼';else if(['zip','rar','7z','tar','gz'].includes(t))s='📦';else if(['xls','xlsx','csv'].includes(t))s='📊';else if(['ppt','pptx'].includes(t))s='📑';else if(t==='pdf')s='PDF';else if(['py','js','ts','html','css','json','yaml','xml','sql','sh','java','c','cpp','go','rs'].includes(t))s='</>';const fs=s.length>2?'7':'10';return`<svg width="22" height="22" viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" fill="${c}" opacity=".12"/><rect x="4" y="2" width="16" height="20" rx="2" stroke="${c}" stroke-width="1.5"/><text x="12" y="15" text-anchor="middle" font-size="${fs}" font-weight="600" fill="${c}">${s}</text></svg>`}

const loading=ref(false),items=ref([]),counts=ref({all:0,approved:0}),activeStatus=ref(''),search=ref(''),currentFolder=ref(null),breadcrumb=ref([]),page=ref(1),totalPages=ref(1),selectedIds=ref(new Set())
const showUpload=ref(false),uploadFile=ref(null),uploading=ref(false),uploadDragover=ref(false),uploadForm=ref({tags:'',description:''})
const showCreateFolder=ref(false),folderName=ref('')
const moveTarget=ref(null),moveParentId=ref('')
const showTrash=ref(false),trashItems=ref([]),trashPage=ref(1),trashTotalPages=ref(1)
const showLogs=ref(false),logItems=ref([]),logPage=ref(1),logTotalPages=ref(1)

function formatSize(b){if(!b)return'-';const u=['B','KB','MB','GB'];let i=0;while(b>=1024&&i<u.length-1){b/=1024;i++};return`${b.toFixed(i>0?1:0)} ${u[i]}`}
function formatDate(iso){if(!iso)return'-';const d=new Date(iso+'Z');const p=n=>String(n).padStart(2,'0');return`${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}`}
function statusLabel(s){const m={approved:'已通过',pending:'待审核',rejected:'已拒绝'};return m[s]||s}
function actionLabel(a){const m={upload:'上传',download:'下载',delete:'删除',restore:'恢复',rename:'重命名',move:'移动'};return m[a]||a}
function toggleSelect(id){const s=new Set(selectedIds.value);s.has(id)?s.delete(id):s.add(id);selectedIds.value=s}

let st=null
function debouncedLoad(){clearTimeout(st);st=setTimeout(()=>{page.value=1;loadResources()},300)}
async function loadResources(){loading.value=true;try{const p={page:page.value,per_page:20};if(search.value){p.search=search.value}else{if(currentFolder.value)p.parent_id=currentFolder.value}if(activeStatus.value)p.status=activeStatus.value;const d=await getAdminResources(p);items.value=d.items;totalPages.value=d.pages;counts.value=d.counts||{};breadcrumb.value=d.breadcrumb||[]}catch(e){console.error(e)}finally{loading.value=false}}
function navigateTo(id){currentFolder.value=id;page.value=1;loadResources()}

function handleUploadDrop(e){uploadDragover.value=false;const f=e.dataTransfer?.files?.[0];if(f)uploadFile.value=f}
function handleFileSelect(e){const f=e.target.files?.[0];if(f)uploadFile.value=f}
async function handleUpload(){if(!uploadFile.value)return;uploading.value=true;try{const fd=new FormData();fd.append('file',uploadFile.value);if(currentFolder.value)fd.append('parent_id',currentFolder.value);if(uploadForm.value.tags)fd.append('tags',JSON.stringify(uploadForm.value.tags.split(',').map(t=>t.trim()).filter(Boolean)));if(uploadForm.value.description)fd.append('description',uploadForm.value.description);await uploadResource(fd);showUpload.value=false;uploadFile.value=null;uploadForm.value={tags:'',description:''};loadResources()}catch(e){alert(e.message||'上传失败')}finally{uploading.value=false}}
async function handleCreateFolder(){if(!folderName.value.trim())return;try{await createFolder({name:folderName.value.trim(),parent_id:currentFolder.value});showCreateFolder.value=false;folderName.value='';loadResources()}catch(e){alert(e.message||'创建失败')}}
async function updateStatus(id,s){try{await updateResourceStatus(id,s);loadResources()}catch(e){alert(e.message||'操作失败')}}
const sortedFolders=ref([])
async function openMove(id){moveTarget.value=id;moveParentId.value='';try{const d=await getAdminFolders();const all=d.folders||[];const exclude=new Set();exclude.add(id);let changed=true;while(changed){changed=false;for(const f of all){if(!exclude.has(f.id)&&exclude.has(f.parent_id)){exclude.add(f.id);changed=true}}}const valid=all.filter(f=>!exclude.has(f.id));const childrenMap=new Map();for(const f of valid){if(!childrenMap.has(f.parent_id))childrenMap.set(f.parent_id,[]);childrenMap.get(f.parent_id).push(f)}const result=[];function walk(parentId,depth){const children=(childrenMap.get(parentId)||[]).sort((a,b)=>a.name.localeCompare(b.name));for(const c of children){result.push({...c,depth,hasChildren:childrenMap.has(c.id)});walk(c.id,depth+1)}}walk(null,0);sortedFolders.value=result}catch{sortedFolders.value=[]}}
async function handleMove(){try{await moveResource(moveTarget.value,moveParentId.value?parseInt(moveParentId.value):null);moveTarget.value=null;loadResources()}catch(e){alert(e.message||'移动失败')}}
async function deleteSingle(item){if(!confirm(`确定删除「${item.name}」？`))return;try{await deleteResource(item.id);loadResources()}catch(e){alert(e.message||'删除失败')}}
async function loadTrash(){try{const d=await getTrash({page:trashPage.value,per_page:50});trashItems.value=d.items;trashTotalPages.value=d.pages}catch(e){console.error(e)}}
async function restoreItem(id){try{await restoreResource(id);loadTrash();loadResources()}catch(e){alert(e.message||'恢复失败')}}
async function permanentDelete(id){if(!confirm('确定永久删除？'))return;try{await permanentDeleteResource(id);loadTrash()}catch(e){alert(e.message||'删除失败')}}
async function loadLogs(){try{const d=await getResourceLogs({page:logPage.value,per_page:50});logItems.value=d.items;logTotalPages.value=d.pages}catch(e){console.error(e)}}
async function batchAction(action){const ids=[...selectedIds.value];if(!ids.length)return;if(action==='delete'&&!confirm(`确定删除 ${ids.length} 项？`))return;try{await batchResources({ids,action});selectedIds.value.clear();loadResources()}catch(e){alert(e.message||'操作失败')}}

onMounted(loadResources)
</script>

<style scoped>
/* ---- root ---- */
.rm-root{display:flex;flex-direction:column;gap:14px}

/* ---- 统计卡片 ---- */
.rm-stats-row{display:flex;gap:10px;flex-wrap:wrap}
.rm-stat-card{position:relative;flex:1;min-width:100px;padding:14px 18px;background:white;border:1px solid var(--glass-border);border-radius:var(--radius-lg);cursor:pointer;transition:all .15s;display:flex;flex-direction:column;gap:4px;overflow:hidden}
.rm-stat-card:hover{border-color:var(--warm-terracotta);box-shadow:var(--shadow-sm)}
.rm-stat-card.active{border-color:var(--warm-terracotta);box-shadow:0 0 0 1px rgba(192,96,64,.15)}
.rm-stat-card.brand{background:linear-gradient(135deg,rgba(192,96,64,.04),white)}
.rm-stat-num{font-family:var(--font-heading);font-size:22px;font-weight:700;color:var(--text-primary)}
.rm-stat-card.active .rm-stat-num{color:var(--warm-terracotta)}
.rm-stat-label{font-size:11px;color:var(--text-muted);font-weight:500}
.rm-stat-bar{position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--warm-terracotta);opacity:0;transition:all .2s}
.rm-stat-card.active .rm-stat-bar{opacity:1}

/* ---- 工具栏 ---- */
.rm-toolbar{display:flex;align-items:center;gap:10px;background:white;border:1px solid var(--glass-border);border-radius:var(--radius-lg);padding:10px 14px;flex-wrap:wrap}
.rm-search-wrap{display:flex;align-items:center;gap:6px;flex:1;min-width:140px;background:var(--bg-soft);border-radius:var(--radius-md);padding:0 10px;border:1px solid transparent;transition:all .2s}
.rm-search-wrap:focus-within{border-color:var(--warm-terracotta);background:white}
.rm-search-icon{color:var(--text-muted);flex-shrink:0}
.rm-search{border:none;background:none;padding:8px 0;font-size:12px;outline:none;width:100%}
.rm-select{padding:7px 10px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:12px;background:white}
.rm-actions{display:flex;gap:6px;margin-left:auto}

/* ---- 面包屑 ---- */
.rm-breadcrumb{display:flex;align-items:center;gap:4px;font-size:12px}
.rm-bc-link{display:inline-flex;align-items:center;gap:4px;padding:4px 8px;border:none;background:none;color:var(--text-muted);cursor:pointer;border-radius:4px;transition:all .15s}
.rm-bc-link:hover{color:var(--warm-terracotta);background:rgba(192,96,64,.04)}
.rm-bc-link.active{color:var(--text-primary);font-weight:600}
.rm-bc-chevron{color:var(--text-muted)}

/* ---- 批量栏 ---- */
.rm-batch{display:flex;align-items:center;gap:8px;padding:10px 16px;background:linear-gradient(135deg,rgba(192,96,64,.06),rgba(212,146,10,.04));border:1px solid rgba(192,96,64,.12);border-radius:var(--radius-lg)}
.rm-batch-badge{background:var(--warm-terracotta);color:white;font-weight:700;font-size:12px;min-width:24px;height:24px;border-radius:12px;display:flex;align-items:center;justify-content:center}
.rm-batch-text{font-size:12px;font-weight:500}

/* ---- 加载/空 ---- */
.rm-loading{display:flex;align-items:center;gap:10px;justify-content:center;padding:48px 0;color:var(--text-muted);font-size:13px}
.rm-spinner{width:22px;height:22px;border:2px solid var(--glass-border);border-top-color:var(--warm-terracotta);border-radius:50%;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.rm-empty{text-align:center;padding:48px 0;color:var(--text-muted);font-size:13px}

/* ---- 列表 ---- */
.rm-list{background:white;border:1px solid var(--glass-border);border-radius:var(--radius-lg);overflow:hidden}
.rm-row{display:flex;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid rgba(0,0,0,.03);transition:all .12s;cursor:default}
.rm-row:last-child{border-bottom:none}
.rm-row:hover{background:var(--bg-soft)}
.rm-row.folder{cursor:pointer}
.rm-row.folder:hover{background:rgba(245,166,35,.04)}
.rm-row.selected{background:rgba(192,96,64,.03);border-left:3px solid var(--warm-terracotta);padding-left:13px}
.rm-cb{flex-shrink:0}
.rm-cb input{accent-color:var(--warm-terracotta);cursor:pointer}
.rm-icon{flex-shrink:0;display:flex;align-items:center}
.rm-info{flex:1;min-width:0}
.rm-row-top{display:flex;align-items:center;gap:8px;margin-bottom:4px;flex-wrap:wrap}
.rm-name{font-size:13px;font-weight:600}
.rm-badge{font-size:10px;padding:2px 8px;border-radius:999px;font-weight:600}
.badge-approved{background:rgba(46,125,50,.1);color:#2e7d32}
.badge-pending{background:rgba(230,81,0,.1);color:#e65100}
.badge-rejected{background:rgba(198,40,40,.1);color:#c62828}
.rm-row-meta{display:flex;gap:12px;font-size:11px;color:var(--text-muted);flex-wrap:wrap}
.rm-folder-path{color:var(--warm-terracotta);font-weight:500}
.rm-row-actions{display:flex;gap:3px;flex-shrink:0}

/* ---- 图标按钮 ---- */
.rm-icon-btn{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border:none;background:none;color:var(--text-muted);cursor:pointer;border-radius:6px;transition:all .12s}
.rm-icon-btn:hover{background:var(--bg-soft);color:var(--warm-terracotta)}
.rm-icon-btn.green:hover{color:#2e7d32;background:rgba(46,125,50,.08)}
.rm-icon-btn.orange:hover{color:#e65100;background:rgba(230,81,0,.08)}
.rm-icon-btn.red:hover{color:#c62828;background:rgba(198,40,40,.08)}

/* ---- 按钮 ---- */
.rm-btn{display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:var(--radius-md);font-size:12px;font-weight:500;cursor:pointer;border:none;transition:all .15s}
.rm-btn:disabled{opacity:.5;cursor:not-allowed}
.rm-btn.primary{background:var(--grad-primary);color:white}
.rm-btn.primary:hover:not(:disabled){opacity:.9}
.rm-btn.outline{background:white;border:1px solid var(--glass-border);color:var(--text-primary)}
.rm-btn.outline:hover:not(:disabled){border-color:var(--warm-terracotta);color:var(--warm-terracotta)}
.rm-btn.text{background:none;border:none;color:var(--text-muted);padding:6px 10px}
.rm-btn.text:hover{color:var(--text-primary)}
.rm-btn.red{color:#c62828}
.rm-btn.red:hover{border-color:#c62828;color:#c62828}
.rm-btn.orange:hover{border-color:#e65100;color:#e65100}
.rm-btn.green:hover{border-color:#2e7d32;color:#2e7d32}
.rm-btn.sm{padding:4px 10px;font-size:11px}

/* ---- 分页 ---- */
.rm-pagination{display:flex;align-items:center;justify-content:center;gap:10px;padding:8px 0}
.rm-page-btn{display:inline-flex;align-items:center;gap:4px;padding:6px 14px;border:1px solid var(--glass-border);background:white;border-radius:var(--radius-md);font-size:12px;cursor:pointer;transition:all .15s}
.rm-page-btn:hover:not(:disabled){border-color:var(--warm-terracotta);color:var(--warm-terracotta)}
.rm-page-btn:disabled{opacity:.4;cursor:not-allowed}
.rm-page-info{font-size:12px;color:var(--text-muted)}

/* ---- 弹窗 ---- */
.rm-modal-mask{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px}
.rm-modal{background:white;border-radius:var(--radius-xl);width:100%;max-width:520px;max-height:88vh;display:flex;flex-direction:column;box-shadow:0 25px 60px rgba(0,0,0,.15)}
.rm-modal-sm{max-width:400px}
.rm-modal-lg{max-width:800px}
.rm-modal-hd{display:flex;align-items:center;justify-content:space-between;padding:16px 22px;border-bottom:1px solid var(--glass-border)}
.rm-modal-hd h3{font-family:var(--font-heading);font-size:15px;font-weight:600;margin:0}
.rm-modal-x{background:none;border:none;color:var(--text-muted);cursor:pointer;padding:4px;border-radius:6px;display:flex;transition:all .15s}
.rm-modal-x:hover{background:var(--bg-soft);color:var(--text-primary)}
.rm-modal-bd{padding:22px;overflow-y:auto;flex:1}
.rm-modal-ft{display:flex;justify-content:flex-end;gap:8px;padding:12px 22px;border-top:1px solid var(--glass-border);background:var(--bg-soft)}

/* ---- 移动树形列表 ---- */
.rm-move-label{font-size:12px;color:var(--text-muted);font-weight:500;margin-bottom:8px}
.rm-move-tree{max-height:300px;overflow-y:auto;border:1px solid var(--glass-border);border-radius:var(--radius-md);background:white}
.rm-move-item{display:flex;align-items:center;gap:8px;padding:8px 14px;font-size:13px;cursor:pointer;transition:all .12s;border-bottom:1px solid rgba(0,0,0,.03)}
.rm-move-item:last-child{border-bottom:none}
.rm-move-item:hover{background:var(--bg-soft)}
.rm-move-item.active{background:rgba(192,96,64,.08);color:var(--warm-terracotta);font-weight:600}
.rm-move-icon{font-size:14px;flex-shrink:0}

/* ---- 上传区 ---- */
.rm-dropzone{border:2px dashed var(--glass-border);border-radius:var(--radius-lg);padding:40px;text-align:center;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:10px;margin-bottom:18px;transition:all .2s}
.rm-dropzone:hover,.rm-dropzone.on{border-color:var(--warm-terracotta);background:rgba(192,96,64,.02)}

/* ---- 表单 ---- */
.rm-fields{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.rm-field{display:flex;flex-direction:column}
.rm-field.full{grid-column:1/-1}
.rm-field span{font-size:12px;font-weight:500;color:var(--text-muted);margin-bottom:5px}
.rm-field input,.rm-field select,.rm-field textarea{padding:9px 12px;border:1px solid var(--glass-border);border-radius:var(--radius-md);font-size:13px;background:white;font-family:inherit;transition:border-color .15s}
.rm-field input:focus,.rm-field select:focus,.rm-field textarea:focus{outline:none;border-color:var(--warm-terracotta);box-shadow:0 0 0 3px rgba(192,96,64,.06)}

/* ---- 回收站/日志 ---- */
.rm-simple-list{display:flex;flex-direction:column;gap:6px}
.rm-simple-row{display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--bg-soft);border-radius:var(--radius-md);font-size:12px}
.rm-simple-name{flex:1;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.rm-log-row{display:flex;align-items:center;gap:10px;padding:10px 14px;font-size:12px;border-bottom:1px solid rgba(0,0,0,.03)}
.rm-log-badge{padding:2px 8px;border-radius:4px;font-size:10px;font-weight:600}
.rm-log-name{flex:1;font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lg-upload{background:rgba(46,125,50,.1);color:#2e7d32}
.lg-download{background:rgba(33,115,70,.1);color:#217346}
.lg-delete{background:rgba(198,40,40,.1);color:#c62828}
.lg-restore{background:rgba(33,150,243,.1);color:#1976d2}
.lg-rename{background:rgba(230,81,0,.1);color:#e65100}
.lg-move{background:rgba(156,39,176,.1);color:#9c27b0}

.text-muted{font-size:11px;color:var(--text-muted)}

@media(max-width:768px){
  .rm-stats-row{gap:6px}
  .rm-stat-card{min-width:70px;padding:10px 12px}
  .rm-stat-num{font-size:18px}
  .rm-row-meta{gap:6px}
}
</style>
